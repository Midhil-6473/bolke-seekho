// Voice recording: 16 kHz mono WAV for Gnani Prisma.
// Port of the recorder in templates/index.html — same merge /
// downsample / WAV-encoding behaviour, same ScriptProcessor setup,
// same amplitude loop feeding the orb.

function merge(buffers) {
  let len = 0;
  buffers.forEach((b) => {
    len += b.length;
  });
  const out = new Float32Array(len);
  let off = 0;
  buffers.forEach((b) => {
    out.set(b, off);
    off += b.length;
  });
  return out;
}

function downsample(buf, inRate, outRate) {
  if (inRate === outRate) return buf;
  const ratio = inRate / outRate;
  const newLen = Math.round(buf.length / ratio);
  const out = new Float32Array(newLen);
  for (let i = 0; i < newLen; i++) {
    const start = Math.round(i * ratio);
    const end = Math.round((i + 1) * ratio);
    let sum = 0;
    let n = 0;
    for (let j = start; j < end && j < buf.length; j++) {
      sum += buf[j];
      n++;
    }
    out[i] = n ? sum / n : 0;
  }
  return out;
}

function encodeWav(samples, rate) {
  const buffer = new ArrayBuffer(44 + samples.length * 2);
  const v = new DataView(buffer);
  const wstr = (o, s) => {
    for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i));
  };
  wstr(0, 'RIFF');
  v.setUint32(4, 36 + samples.length * 2, true);
  wstr(8, 'WAVEfmt ');
  v.setUint32(16, 16, true);
  v.setUint16(20, 1, true);
  v.setUint16(22, 1, true);
  v.setUint32(24, rate, true);
  v.setUint32(28, rate * 2, true);
  v.setUint16(32, 2, true);
  v.setUint16(34, 16, true);
  wstr(36, 'data');
  v.setUint32(40, samples.length * 2, true);
  let off = 44;
  for (let i = 0; i < samples.length; i++, off += 2) {
    const s = Math.max(-1, Math.min(1, samples[i]));
    v.setInt16(off, s < 0 ? s * 0x8000 : s * 0x7fff, true);
  }
  return new Blob([buffer], { type: 'audio/wav' });
}

export function recordingSupported() {
  return !!(
    navigator.mediaDevices &&
    navigator.mediaDevices.getUserMedia &&
    (window.AudioContext || window.webkitAudioContext)
  );
}

export class Recorder {
  constructor({ onAmp, onTick }) {
    this.onAmp = onAmp || (() => {});
    this.onTick = onTick || (() => {});
    this.buffers = null;
    this.processor = null;
    this.source = null;
    this.analyser = null;
    this.stream = null;
    this.audioCtx = null;
    this.sampleRate = 0;
    this.rafId = 0;
    this.timerId = null;
    this.startedAt = 0;
    this.stopped = false;
  }

  async start() {
    let stream;
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const source = audioCtx.createMediaStreamSource(stream);
      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 512;
      source.connect(analyser);
      const processor = audioCtx.createScriptProcessor(4096, 1, 1);
      const buffers = [];
      processor.onaudioprocess = (e) => buffers.push(new Float32Array(e.inputBuffer.getChannelData(0)));
      source.connect(processor);
      processor.connect(audioCtx.destination);
      this.buffers = buffers;
      this.processor = processor;
      this.source = source;
      this.analyser = analyser;
      this.stream = stream;
      this.audioCtx = audioCtx;
      this.sampleRate = audioCtx.sampleRate;
    } catch (err) {
      if (stream) stream.getTracks().forEach((tr) => tr.stop());
      throw err;
    }
    const dataArr = new Uint8Array(this.analyser.frequencyBinCount);
    const loop = () => {
      if (this.stopped) return;
      this.analyser.getByteTimeDomainData(dataArr);
      let peak = 0;
      for (let i = 0; i < dataArr.length; i++) {
        peak = Math.max(peak, Math.abs(dataArr[i] - 128) / 128);
      }
      this.onAmp(peak);
      this.rafId = requestAnimationFrame(loop);
    };
    loop();
    this.startedAt = Date.now();
    const tick = () => {
      const s = Math.floor((Date.now() - this.startedAt) / 1000);
      this.onTick(Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'));
    };
    tick();
    this.timerId = setInterval(tick, 500);
  }

  // Stops recording and returns the 16 kHz mono WAV blob, or null if
  // recording never started.
  stop() {
    if (this.stopped || !this.buffers) return null;
    this.stopped = true;
    if (this.rafId) cancelAnimationFrame(this.rafId);
    if (this.timerId) clearInterval(this.timerId);
    this.timerId = null;
    this.onAmp(0);
    try {
      this.processor.disconnect();
      this.source.disconnect();
      this.stream.getTracks().forEach((tr) => tr.stop());
      this.audioCtx.close();
    } catch (e) {
      /* already torn down */
    }
    return encodeWav(downsample(merge(this.buffers), this.sampleRate, 16000), 16000);
  }
}
