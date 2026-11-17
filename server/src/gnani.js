// Gnani Prisma (speech-to-text) + Timbre (text-to-speech) REST calls.
//
// Replicates the wire behaviour of gnani-vachana 0.10.0
// (GnaniSTTClient.transcribe and GnaniTTSClient.synthesize) using
// fetch: same base URL, endpoints, auth/request-ID headers, payloads,
// timeouts and response parsing. The API key is never logged.

import { randomUUID } from 'node:crypto';

const BASE_URL = 'https://api.vachana.ai';
const STT_ENDPOINT = '/stt/v3';
const TTS_ENDPOINT = '/api/v1/tts/inference';
const TIMEOUT_MS = 60000;

// Mirrors the SDK's APIError: str(exc) is "HTTP <status>: <body>".
export class APIError extends Error {
  constructor(statusCode, body) {
    super(`HTTP ${statusCode}: ${body}`);
    this.name = 'APIError';
    this.statusCode = statusCode;
    this.body = body;
  }
}

// Mirrors gnani.log.resolve_request_id: "req_" + 12 hex chars.
function newRequestId() {
  return `req_${randomUUID().replace(/-/g, '').slice(0, 12)}`;
}

async function postWithTimeout(url, options) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

// GnaniSTTClient(api_key).transcribe(wav_file, language_code=...):
// POST {base}/stt/v3, multipart field "audio_file" plus form fields
// language_code and format="verbatim". Returns the parsed JSON dict.
export async function transcribe(audioBytes, languageCode, apiKey) {
  const form = new FormData();
  form.append(
    'audio_file',
    new Blob([audioBytes], { type: 'audio/wav' }),
    'audio.wav',
  );
  form.append('language_code', languageCode);
  form.append('format', 'verbatim');
  const resp = await postWithTimeout(`${BASE_URL}${STT_ENDPOINT}`, {
    method: 'POST',
    headers: {
      'X-API-Key-ID': apiKey,
      'X-API-Request-ID': newRequestId(),
    },
    body: form,
  });
  if (resp.status !== 200) {
    throw new APIError(resp.status, await resp.text());
  }
  return resp.json();
}

// GnaniTTSClient(api_key).synthesize(text, voice=..., model="timbre-v2.5",
// language=..., audio_config=AudioConfig(container="mp3",
// sample_rate=48000, bitrate="128k")):
// POST {base}/api/v1/tts/inference with a JSON body. Returns raw audio bytes.
export async function synthesize(text, { voice, language, apiKey }) {
  const body = {
    text,
    model: 'timbre-v2.5',
    audio_config: {
      sample_rate: 48000,
      encoding: 'linear_pcm',
      num_channels: 1,
      sample_width: 2,
      container: 'mp3',
      bitrate: '128k',
    },
    voice,
    language,
    speed: 1.0, // timbre-v2.5 default when speed is not given
  };
  const resp = await postWithTimeout(`${BASE_URL}${TTS_ENDPOINT}`, {
    method: 'POST',
    headers: {
      'X-API-Key-ID': apiKey,
      'Content-Type': 'application/json',
      'X-API-Request-ID': newRequestId(),
    },
    body: JSON.stringify(body),
  });
  if (resp.status !== 200) {
    throw new APIError(resp.status, await resp.text());
  }
  return Buffer.from(await resp.arrayBuffer());
}
