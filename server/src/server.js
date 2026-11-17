// Bolke Seekho — Node backend (port of the Flask app.py).
//
// Search any algorithm: the app shows the key code first, then every
// approach with its logic, Java code, time and space complexity, and
// the best technique flagged. Ask follow-up questions about the
// algorithm or one of its methods, and the voice agent answers in
// that context — by text, or spoken aloud when a Gnani API key is set.
//
// 41 algorithms are curated in the approaches bank (key code +
// approaches + best pick). Anything else is answered by a configured
// LLM in the same shape, so students are not limited to a fixed list.
// Voice uses Gnani Prisma (speech-to-text) and Timbre (text-to-speech)
// in 10 languages.
//
// Set GNANI_API_KEY (from app.gnani.ai) in the environment or in a .env
// file at the project root. For open-ended answers, also set
// BOLKE_LLM_BASE_URL, BOLKE_LLM_MODEL and optionally BOLKE_LLM_API_KEY
// (any OpenAI-compatible chat API).
// Run:  npm start   then open http://127.0.0.1:5000

import express from 'express';
import multer from 'multer';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  LANGUAGES,
  ALGORITHMS,
  answerLangFor,
  answerQuery,
  findFollowup,
  findAlgorithm,
  suggestAlgorithms,
} from './bank.js';
import { llmAnswer, llmFollowup, llmStructured } from './llm.js';
import { transcribe as gnaniTranscribe, synthesize as gnaniSynthesize } from './gnani.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
const PUBLIC_DIR = path.resolve(__dirname, '..', 'public');

function loadDotenv() {
  const envPath = path.join(PROJECT_ROOT, '.env');
  if (!fs.existsSync(envPath)) return;
  const content = fs.readFileSync(envPath, 'utf-8');
  for (const rawLine of content.split('\n')) {
    const line = rawLine.trim();
    if (line && !line.startsWith('#') && line.includes('=')) {
      const idx = line.indexOf('=');
      const k = line.slice(0, idx).trim();
      const v = line.slice(idx + 1).trim();
      if (!(k in process.env)) process.env[k] = v;
    }
  }
}

loadDotenv();
const API_KEY = (process.env.GNANI_API_KEY || '').trim();
const TTS_VOICE = (process.env.BOLKE_TTS_VOICE || 'Nalini').trim() || 'Nalini';

// Timbre language parameter per answer language ("auto" lets it detect
// from the text; Roman Hinglish works best as auto).
const TTS_LANG = {
  hinglish: 'auto',
  english: 'en-IN',
  telugu: 'te-IN',
  tamil: 'ta-IN',
  kannada: 'kn-IN',
  malayalam: 'ml-IN',
};

function bankLang(lang) {
  return answerLangFor(lang in LANGUAGES ? lang : 'hinglish');
}

// Gnani Prisma (speech-to-text) in the chosen language.
async function transcribe(audioBytes, lang) {
  const languageCode = LANGUAGES[lang] || 'hi-IN';
  const result = await gnaniTranscribe(audioBytes, languageCode, API_KEY);
  if (result !== null && typeof result === 'object') {
    return result.transcript || '';
  }
  return (result && result.text) || '';
}

// Gnani Timbre v2.5 (text-to-speech) in the answer's language, MP3 out.
async function speak(text, lang) {
  const bank = bankLang(lang);
  return gnaniSynthesize(text, {
    voice: TTS_VOICE,
    language: TTS_LANG[bank] || 'auto',
    apiKey: API_KEY,
  });
}

// Text answer plus spoken audio when a key is set.
//
// Without a key, the text answer still works and voice_available is
// False, so the search bar never looks dead just because voice is off.
async function spokenPayload(text, lang, topic = '') {
  if (!API_KEY) {
    return { topic, answer: text, audio_base64: '', tts_error: '', voice_available: false };
  }
  try {
    const audio = await speak(text, lang);
    return {
      topic,
      answer: text,
      audio_base64: audio.toString('base64'),
      tts_error: '',
      voice_available: true,
    };
  } catch (err) {
    // Keep the text answer usable even if TTS fails.
    return {
      topic,
      answer: text,
      audio_base64: '',
      tts_error: `${err.name}: ${err.message}`,
      voice_available: false,
    };
  }
}

// Approaches-bank entry by exact name (case-insensitive), or null.
function bankEntry(name) {
  const wanted = (name || '').trim().toLowerCase();
  if (!wanted) return null;
  return ALGORITHMS.find((entry) => entry.name.toLowerCase() === wanted) || null;
}

// Search one question: curated algorithm, LLM algorithm, or answer.
//
// Curated matches answer from the approaches bank (checked key code +
// approaches). Anything else goes to the LLM, first asking for the same
// structured shape, then for a plain answer. When no LLM is configured
// or it fails, the bank's family guide / not-in-list text is returned.
async function search(question, lang) {
  const entry = findAlgorithm(question);
  if (entry !== null) {
    const result = {
      kind: 'algorithm',
      source: 'bank',
      name: entry.name,
      category: entry.category,
      key_logic: entry.key_logic,
      approaches: entry.approaches,
      llm: false,
    };
    result.summary = spokenSummary(result, lang);
    return result;
  }
  const structured = await llmStructured(question, lang);
  if (structured !== null) {
    structured.kind = 'algorithm';
    structured.source = 'llm';
    structured.llm = true;
    structured.summary = spokenSummary(structured, lang);
    return structured;
  }
  const text = await llmAnswer(question, lang);
  if (text) {
    const result = {
      kind: 'answer',
      source: 'llm',
      topic: 'AI answer',
      answer: text,
      category: 'Open DSA question',
      matched: false,
      family: '',
      suggestions: [],
      llm: true,
    };
    result.summary = spokenSummary(result, lang);
    return result;
  }
  const result = answerQuery(question, lang);
  const out = {
    kind: 'answer',
    source: 'bank',
    topic: result.topic,
    answer: result.answer,
    category: result.category,
    matched: result.matched,
    family: result.family || '',
    suggestions: result.suggestions,
    llm: false,
  };
  out.summary = spokenSummary(out, lang);
  return out;
}

// What the voice agent says after a voice search.
//
// Curated algorithms get the bank's spoken pattern-style answer in the
// user's language. LLM algorithms get their key logic plus the best
// approach. Plain answers are spoken as they are.
function spokenSummary(result, lang) {
  if (result.kind === 'answer') return result.answer;
  if (result.source === 'bank') {
    const bank = answerQuery(result.name, lang);
    if (bank.matched && bank.topic === result.name) return bank.answer;
  }
  const best = result.approaches.find((a) => a.optimal) || null;
  let summary = result.key_logic;
  if (best !== null) {
    summary += ` Best approach: ${best.name}, ${best.time} time, ${best.space} space.`;
  }
  return summary;
}

// Answer a question about the algorithm on screen.
//
// Returns [answer_text, llm_used, is_fallback]. With an LLM configured,
// the model answers in the context of the algorithm and its approaches
// (optionally focused on one approach). Without one, the bank's spoken
// answer for the algorithm is the best available context answer.
async function followupAnswer(question, lang, algorithm, approach, clientApproaches) {
  const entry = bankEntry(algorithm);
  const approaches = entry !== null ? entry.approaches : clientApproaches || [];
  const text = await llmFollowup(question, lang, algorithm, approaches, approach);
  if (text) return [text, true, false];
  const bank = answerQuery(algorithm, lang);
  return [bank.answer, false, true];
}

/* ------------------------------------------------------------------ */
/* HTTP layer                                                          */
/* ------------------------------------------------------------------ */

const app = express();

// Parse a JSON body the way Flask's get_json(force=True, silent=True)
// does: any content type, {} on failure or empty body.
function parseJsonBody(req) {
  const buf = req.body;
  if (!buf || !buf.length) return {};
  try {
    const data = JSON.parse(buf.toString('utf-8'));
    return data !== null && typeof data === 'object' && !Array.isArray(data) ? data : {};
  } catch {
    return {};
  }
}
const rawBody = express.raw({ type: '*/*', limit: '10mb' });

// Like Python int(): optional sign, digits, surrounding whitespace.
function parseLimit(raw) {
  const s = String(raw);
  if (!/^\s*[+-]?\d+\s*$/.test(s)) return null;
  return Number.parseInt(s.trim(), 10);
}

const upload = multer({ storage: multer.memoryStorage() });

// Flask's request.args.get / request.form.get return the FIRST value
// when a field repeats; Express may hand us an array. Match Flask.
function firstOf(value, fallback) {
  if (Array.isArray(value)) return value.length ? value[0] : fallback;
  return value === undefined ? fallback : value;
}

app.get('/api/config', (req, res) => {
  res.json({ key_set: Boolean(API_KEY), languages: Object.keys(LANGUAGES) });
});

app.get('/api/suggest', (req, res) => {
  const query = String(firstOf(req.query.q, '')).trim();
  let limit = 6;
  const rawLimit = firstOf(req.query.limit, undefined);
  if (rawLimit !== undefined && rawLimit !== '') {
    const parsed = parseLimit(rawLimit);
    limit = parsed === null ? 6 : parsed;
  }
  limit = Math.max(1, Math.min(limit, 10));
  res.json({ suggestions: suggestAlgorithms(query, limit) });
});

app.post('/api/search', rawBody, async (req, res) => {
  // Typed search. Works without an API key (text only).
  const data = parseJsonBody(req);
  const question = (data.question || '').trim();
  const lang = String(data.lang || 'hinglish').toLowerCase();
  if (!question) {
    return res.status(400).json({ error: 'Type an algorithm to search for first.', error_code: 'EMPTY_QUESTION' });
  }
  const result = await search(question, lang);
  result.voice_available = Boolean(API_KEY);
  result.answer_lang = bankLang(lang);
  res.json(result);
});

app.post('/api/ask', (req, res) => {
  // Voice search / voice follow-up. Needs a Gnani API key.
  //
  // Without an `algorithm` form field, the transcript is a fresh search
  // and the spoken summary is returned with the result. With one, the
  // transcript is a follow-up question about that algorithm (optionally
  // focused on one `approach`), answered in context and spoken aloud.
  upload.single('audio')(req, res, async (multerErr) => {
    if (!API_KEY) {
      return res.status(400).json({
        error: 'Voice needs a Gnani API key. Add GNANI_API_KEY to the .env file and restart — typed questions work without it.',
        error_code: 'NO_API_KEY',
      });
    }
    if (multerErr) {
      return res.status(400).json({ error: 'No audio received.', error_code: 'NO_AUDIO' });
    }
    const lang = String(firstOf(req.body && req.body.lang, 'hinglish')).toLowerCase();
    const file = req.file;
    if (!file) {
      return res.status(400).json({ error: 'No audio received.', error_code: 'NO_AUDIO' });
    }
    const audioBytes = file.buffer;
    if (!audioBytes || !audioBytes.length) {
      return res.status(400).json({
        error: 'Empty recording. Hold the mic button, speak, then tap again to stop.',
        error_code: 'EMPTY_AUDIO',
      });
    }
    let transcript;
    try {
      transcript = await transcribe(audioBytes, lang);
    } catch (err) {
      return res.status(502).json({
        error: `Speech-to-text failed: ${err.name}: ${err.message}`,
        error_code: 'STT_FAILED',
      });
    }
    if (!transcript.trim()) {
      return res.status(422).json({
        error: 'Prisma returned an empty transcript. Try speaking again, closer to the mic, or type the question instead.',
        error_code: 'EMPTY_TRANSCRIPT',
      });
    }
    const algorithm = String(firstOf(req.body && req.body.algorithm, '')).trim();
    const approach = String(firstOf(req.body && req.body.approach, '')).trim();
    let clientApproaches = [];
    const rawApproaches = String(firstOf(req.body && req.body.approaches, '')).trim();
    if (rawApproaches) {
      try {
        const parsed = JSON.parse(rawApproaches);
        if (Array.isArray(parsed)) clientApproaches = parsed;
      } catch {
        clientApproaches = [];
      }
    }
    if (algorithm) {
      const [answer, llmUsed, fallback] = await followupAnswer(transcript, lang, algorithm, approach, clientApproaches);
      const payload = await spokenPayload(answer, lang, algorithm);
      return res.json({
        ...payload,
        kind: 'followup',
        transcript,
        algorithm,
        approach,
        llm: llmUsed,
        fallback,
        answer_lang: bankLang(lang),
      });
    }
    const result = await search(transcript, lang);
    const summary = spokenSummary(result, lang);
    const payload = await spokenPayload(summary, lang, result.name || result.topic || '');
    res.json({
      ...payload,
      ...result,
      transcript,
      spoken_summary: summary,
      answer_lang: bankLang(lang),
    });
  });
});

app.post('/api/followup', rawBody, async (req, res) => {
  // Follow-up question about the algorithm on screen.
  //
  // Body: {question, lang, algorithm, approach?, approaches?}. With an
  // LLM configured the answer is context-aware; without one, the bank's
  // answer for the algorithm is returned as a fallback. Spoken audio is
  // included when a Gnani key is set. The legacy {topic, kind} form
  // (simple/example clarifications) is still honoured.
  const data = parseJsonBody(req);
  const lang = String(data.lang || 'hinglish').toLowerCase();
  if ('kind' in data && !((data.question || '').trim())) {
    const topic = (data.topic || '').trim();
    let kind = (data.kind || 'simple').trim();
    if (!topic) {
      return res.status(400).json({ error: 'No topic to clarify.', error_code: 'NO_TOPIC' });
    }
    if (kind !== 'simple' && kind !== 'example') kind = 'simple';
    const text = findFollowup(topic, kind, lang);
    const payload = await spokenPayload(text, lang, topic);
    return res.json({ ...payload, kind, answer_lang: bankLang(lang) });
  }
  const question = (data.question || '').trim();
  const algorithm = (data.algorithm || '').trim();
  const approach = (data.approach || '').trim();
  let clientApproaches = data.approaches || [];
  if (!Array.isArray(clientApproaches)) clientApproaches = [];
  if (!question) {
    return res.status(400).json({ error: 'Type a question about the algorithm first.', error_code: 'EMPTY_QUESTION' });
  }
  if (!algorithm) {
    return res.status(400).json({ error: 'Search for an algorithm first, then ask about it.', error_code: 'NO_ALGORITHM' });
  }
  const [answer, llmUsed, fallback] = await followupAnswer(question, lang, algorithm, approach, clientApproaches);
  const payload = await spokenPayload(answer, lang, algorithm);
  res.json({
    ...payload,
    kind: 'followup',
    algorithm,
    approach,
    llm: llmUsed,
    fallback,
    answer_lang: bankLang(lang),
  });
});

app.post('/api/speak', rawBody, async (req, res) => {
  // Speak any text aloud (Listen buttons). Needs a Gnani API key.
  if (!API_KEY) {
    return res.status(400).json({
      error: 'Voice needs a Gnani API key. Add GNANI_API_KEY to the .env file and restart.',
      error_code: 'NO_API_KEY',
    });
  }
  const data = parseJsonBody(req);
  const text = (data.text || '').trim();
  const lang = String(data.lang || 'hinglish').toLowerCase();
  if (!text) {
    return res.status(400).json({ error: 'Nothing to speak.', error_code: 'EMPTY_TEXT' });
  }
  const payload = await spokenPayload(text, lang);
  res.json(payload);
});

// Unknown API route / wrong method for a known API route.
const KNOWN_API_PATHS = new Set(['/api/config', '/api/suggest', '/api/search', '/api/ask', '/api/followup', '/api/speak']);
app.use((req, res, next) => {
  if (req.path.startsWith('/api/')) {
    if (KNOWN_API_PATHS.has(req.path)) {
      return res.status(405).json({ error: 'Wrong method for this API route.', error_code: 'METHOD_NOT_ALLOWED' });
    }
    return res.status(404).json({ error: 'Unknown API route.', error_code: 'NOT_FOUND' });
  }
  return next();
});

// Serve the built React client when it exists (npm run build).
if (fs.existsSync(path.join(PUBLIC_DIR, 'index.html'))) {
  app.use(express.static(PUBLIC_DIR));
  app.get('*', (req, res) => {
    res.sendFile(path.join(PUBLIC_DIR, 'index.html'));
  });
} else {
  app.get('*', (req, res) => {
    res.status(200).type('text/plain').send(
      'Bolke Seekho API is running, but the web client has not been built yet.\n' +
        'Run `npm run build` once, then reopen this page — or run `npm run dev`\n' +
        'and open the Vite dev server URL it prints.\n',
    );
  });
}

const PORT = Number(process.env.PORT || 5000);
app.listen(PORT, '127.0.0.1', () => {
  console.log(`Bolke Seekho running at http://127.0.0.1:${PORT}`);
});
