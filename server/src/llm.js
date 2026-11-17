// Open-ended DSA answers via any OpenAI-compatible chat API.
//
// Faithful port of llm.py: same prompts, same _chat semantics (30 s
// timeout, 64 KB response cap, Bearer header only when a key is set,
// /chat/completions suffix handling, null on any failure), same
// llm_structured validation and exactly-one-optimal coercion.
// The key is never logged. Answers are AI-generated: the UI labels
// them "AI answer".

const LANG_NAMES = {
  hinglish: 'Hinglish (Hindi mixed with English, written in Roman script)',
  english: 'English',
  telugu: 'Telugu',
  tamil: 'Tamil',
  kannada: 'Kannada',
  malayalam: 'Malayalam',
  marathi: 'Marathi',
  bengali: 'Bengali',
  gujarati: 'Gujarati',
  punjabi: 'Punjabi',
};

const SYSTEM_PROMPT =
  'You are Bolke Seekho, a friendly DSA revision tutor for Indian college ' +
  'students. Answer ONLY data structures and algorithms questions. If the ' +
  'question is not about data structures, algorithms, or coding-interview ' +
  'problem solving, reply in one short sentence that you only answer DSA ' +
  'questions. Answer in {language}. Explain the PATTERN first: name it, say ' +
  'why it works in simple words, give the time and space complexity, and ' +
  'end with the trade-off or interview tip. Keep it short and spoken-friendly: ' +
  '4 to 7 short sentences, simple words, plain text with no markdown ' +
  'formatting and no long code. A tiny 3 to 5 line sketch is allowed only ' +
  'if it makes the idea clearer. Never invent problem numbers or company names.';

const STRUCTURED_PROMPT =
  'You are Bolke Seekho, a friendly DSA revision tutor for Indian college ' +
  'students. The student searched for a data structures or algorithms topic. ' +
  'If the search is not about data structures, algorithms, or coding-interview ' +
  'problem solving, reply with exactly this JSON and nothing else: ' +
  '{"refused": true}. Otherwise respond with JSON only — no markdown, no ' +
  'code fences, no extra text — with exactly this shape: ' +
  '{"name": "Algorithm Name", "key_logic": "the core idea in 1-2 sentences, ' +
  'in {language}", "approaches": [{"name": "Approach name", "logic": "how it ' +
  'works in 1-2 sentences, in {language}", "code": "the core Java method only, ' +
  '5-15 lines, assuming import java.util.*", "time": "O(...)", "space": "O(...)", ' +
  '"optimal": true/false}]}. List 2 to 4 genuinely different approaches, ' +
  'from simplest to best. Mark EXACTLY ONE approach optimal=true: the best ' +
  'technique to use in an interview. Write the name and approach names in ' +
  'English; write key_logic and logic in {language}. Keep code short and ' +
  'correct Java. Never invent problem numbers or company names.';

const FOLLOWUP_PROMPT =
  'You are Bolke Seekho, a friendly DSA revision tutor for Indian college ' +
  'students. The student is looking at the algorithm below and asks a ' +
  'follow-up question about it. Answer ONLY about this algorithm and its ' +
  'approaches. If the question is not about data structures or algorithms, ' +
  'reply in one short sentence that you only answer DSA questions. Answer ' +
  'in {language}. Keep it short and spoken-friendly: 3 to 6 short sentences, ' +
  'simple words, plain text with no markdown formatting. Explain the idea, ' +
  'why it works, and the complexity or trade-off when relevant. ' +
  'If the student asks about a specific approach, answer about that approach. ' +
  'Never invent problem numbers or company names.\n\n' +
  'Algorithm: {algorithm}\n' +
  'Approaches on screen:\n{approaches}\n' +
  '{focus}';

function fmt(template, vars) {
  let out = template;
  for (const [key, value] of Object.entries(vars)) {
    out = out.split(`{${key}}`).join(value);
  }
  return out;
}

function config() {
  const base = (process.env.BOLKE_LLM_BASE_URL || '').trim().replace(/\/+$/, '');
  const model = (process.env.BOLKE_LLM_MODEL || '').trim();
  const key = (process.env.BOLKE_LLM_API_KEY || '').trim();
  if (!base || !model) return null;
  const url = base.endsWith('/chat/completions') ? base : `${base}/chat/completions`;
  return { url, model, key };
}

export function llmConfigured() {
  return config() !== null;
}

async function chat(messages, { temperature = 0.3, maxTokens = 600 } = {}) {
  const cfg = config();
  if (cfg === null) return null;
  const headers = { 'Content-Type': 'application/json' };
  if (cfg.key) headers.Authorization = `Bearer ${cfg.key}`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 30000);
  let raw;
  try {
    const resp = await fetch(cfg.url, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        model: cfg.model,
        messages,
        temperature,
        max_tokens: maxTokens,
      }),
      signal: controller.signal,
    });
    // urllib raises on non-2xx; fetch does not — mirror that.
    if (!resp.ok) return null;
    // Mirror resp.read(65536): read at most 64 KB of the body.
    const reader = resp.body.getReader();
    const chunks = [];
    let total = 0;
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      const room = 65536 - total;
      if (room <= 0) break;
      const take = value.subarray(0, room);
      chunks.push(take);
      total += take.length;
      if (value.length > room) break;
    }
    try {
      await reader.cancel();
    } catch {
      /* already closed */
    }
    const buf = new Uint8Array(total);
    let off = 0;
    for (const chunk of chunks) {
      buf.set(chunk, off);
      off += chunk.length;
    }
    raw = new TextDecoder('utf-8', { fatal: true }).decode(buf);
  } catch {
    return null;
  } finally {
    clearTimeout(timer);
  }
  try {
    const data = JSON.parse(raw);
    const text = data.choices[0].message.content;
    const trimmed = (text || '').trim();
    return trimmed || null;
  } catch {
    return null;
  }
}

export async function llmAnswer(question, lang) {
  const language = LANG_NAMES[lang] || 'English';
  return chat(
    [
      { role: 'system', content: fmt(SYSTEM_PROMPT, { language }) },
      { role: 'user', content: question },
    ],
    { maxTokens: 600 },
  );
}

export async function llmStructured(question, lang) {
  const language = LANG_NAMES[lang] || 'English';
  let text = await chat(
    [
      { role: 'system', content: fmt(STRUCTURED_PROMPT, { language }) },
      { role: 'user', content: question },
    ],
    { temperature: 0.2, maxTokens: 1600 },
  );
  if (!text) return null;
  if (text.startsWith('```')) {
    text = text.replace(/^`+/, '').replace(/`+$/, '').trim();
    if (text.toLowerCase().startsWith('json')) text = text.slice(4).trim();
  }
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    return null;
  }
  if (data === null || typeof data !== 'object' || Array.isArray(data) || data.refused) {
    return null;
  }
  const name = (data.name || '').trim();
  const keyLogic = (data.key_logic || '').trim();
  const rawApproaches = data.approaches;
  if (!name || !keyLogic || !Array.isArray(rawApproaches)) return null;
  const approaches = [];
  for (const raw of rawApproaches.slice(0, 5)) {
    if (raw === null || typeof raw !== 'object' || Array.isArray(raw)) continue;
    const approach = {
      name: (raw.name || '').trim(),
      logic: (raw.logic || '').trim(),
      code: (raw.code || '').trim(),
      time: (raw.time || '').trim(),
      space: (raw.space || '').trim(),
      optimal: Boolean(raw.optimal),
    };
    if (approach.name && approach.logic && approach.code) approaches.push(approach);
  }
  if (approaches.length < 2) return null;
  // Exactly one optimal: keep the first marked, else mark the last
  // (models list approaches worst-to-best, so the last is the best bet).
  const marked = approaches.filter((a) => a.optimal);
  if (marked.length > 1) {
    for (const extra of marked.slice(1)) extra.optimal = false;
  } else if (!marked.length) {
    approaches[approaches.length - 1].optimal = true;
  }
  return {
    name,
    category: ((data.category || 'Open DSA question').trim() || 'Open DSA question'),
    key_logic: keyLogic,
    approaches,
  };
}

export async function llmFollowup(question, lang, algorithm, approaches, focus = '') {
  const language = LANG_NAMES[lang] || 'English';
  const summaryLines = [];
  for (const approach of approaches || []) {
    summaryLines.push(
      `- ${approach.name || ''}: ${approach.logic || ''} (Time ${approach.time || '?'}, Space ${approach.space || '?'})`,
    );
  }
  const focusLine = focus ? `The student is asking about this approach: ${focus}\n` : '';
  const system = fmt(FOLLOWUP_PROMPT, {
    language,
    algorithm,
    approaches: summaryLines.join('\n') || '(no approaches listed)',
    focus: focusLine,
  });
  return chat(
    [
      { role: 'system', content: system },
      { role: 'user', content: question },
    ],
    { maxTokens: 600 },
  );
}
