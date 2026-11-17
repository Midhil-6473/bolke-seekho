// Bolke Seekho banks: matching and lookup logic.
//
// Faithful port of answers.py / topics_extra.py / approaches.py.
// Scoring behaviour is identical to the Python originals, including
// the difflib.SequenceMatcher fuzzy ratio used by both matchers.

import { BANK } from './bank-data.js';

export const LANGUAGES = BANK.LANGUAGES;
export const ALGORITHMS = BANK.ALGORITHMS;
const ANSWERS = BANK.ANSWERS;
const ALIASES = BANK.ALIASES;
const ANSWER_LANGS = BANK.ANSWER_LANGS;
const TOPIC_META = BANK.TOPIC_META;
const FALLBACKS = BANK.FALLBACKS;
const FAMILY_GUIDES = BANK.FAMILY_GUIDES;
const FAMILY_CATEGORIES = BANK.FAMILY_CATEGORIES;
const POPULAR = BANK.POPULAR;
const STOPWORDS_ANSWERS = new Set(BANK.STOPWORDS_ANSWERS);
const STOPWORDS_APPROACHES = new Set(BANK.STOPWORDS_APPROACHES);

const MATCH_THRESHOLD = 10.0;

// Length in Unicode code points, matching Python len(str).
const cplen = (s) => Array.from(s).length;

/* ------------------------------------------------------------------ */
/* difflib.SequenceMatcher (CPython), isjunk=None, autojunk=True.      */
/* Operates on code-point arrays so astral characters count the way    */
/* Python counts them.                                                 */
/* ------------------------------------------------------------------ */

function sequenceMatcherRatio(aStr, bStr) {
  const a = Array.from(aStr);
  const b = Array.from(bStr);
  // __chain_b
  const b2j = new Map();
  b.forEach((elt, i) => {
    if (!b2j.has(elt)) b2j.set(elt, []);
    b2j.get(elt).push(i);
  });
  // autojunk: purge over-popular elements when len(b) >= 200
  if (b.length >= 200) {
    const ntest = Math.floor(b.length / 100) + 1;
    for (const [elt, idxs] of b2j) {
      if (idxs.length > ntest) b2j.delete(elt);
    }
  }
  const isBjunk = () => false; // isjunk is None: nothing is junk

  function findLongestMatch(alo, ahi, blo, bhi) {
    let besti = alo;
    let bestj = blo;
    let bestsize = 0;
    let j2len = new Map();
    const nothing = [];
    for (let i = alo; i < ahi; i++) {
      const newj2len = new Map();
      const indices = b2j.get(a[i]) || nothing;
      for (const j of indices) {
        if (j < blo) continue;
        if (j >= bhi) break;
        const k = (j2len.get(j - 1) || 0) + 1;
        newj2len.set(j, k);
        if (k > bestsize) {
          besti = i - k + 1;
          bestj = j - k + 1;
          bestsize = k;
        }
      }
      j2len = newj2len;
    }
    while (
      besti > alo && bestj > blo &&
      !isBjunk(b[bestj - 1]) && a[besti - 1] === b[bestj - 1]
    ) {
      besti -= 1; bestj -= 1; bestsize += 1;
    }
    while (
      besti + bestsize < ahi && bestj + bestsize < bhi &&
      !isBjunk(b[bestj + bestsize]) && a[besti + bestsize] === b[bestj + bestsize]
    ) {
      bestsize += 1;
    }
    return [besti, bestj, bestsize];
  }

  function getMatchingBlocks() {
    const queue = [[0, a.length, 0, b.length]];
    const matchingBlocks = [];
    while (queue.length) {
      const [alo, ahi, blo, bhi] = queue.pop();
      const [i, j, k] = findLongestMatch(alo, ahi, blo, bhi);
      if (k) {
        matchingBlocks.push([i, j, k]);
        if (alo < i && blo < j) queue.push([alo, i, blo, j]);
        if (i + k < ahi && j + k < bhi) queue.push([i + k, ahi, j + k, bhi]);
      }
    }
    matchingBlocks.sort((x, y) => x[0] - y[0] || x[1] - y[1] || x[2] - y[2]);
    let i1 = 0;
    let j1 = 0;
    let k1 = 0;
    const nonAdjacent = [];
    for (const [i2, j2, k2] of matchingBlocks) {
      if (i1 + k1 === i2 && j1 + k1 === j2) {
        k1 += k2;
      } else {
        if (k1) nonAdjacent.push([i1, j1, k1]);
        i1 = i2; j1 = j2; k1 = k2;
      }
    }
    if (k1) nonAdjacent.push([i1, j1, k1]);
    nonAdjacent.push([a.length, b.length, 0]);
    return nonAdjacent;
  }

  const matches = getMatchingBlocks().reduce((sum, t) => sum + t[2], 0);
  const total = a.length + b.length;
  return total ? (2.0 * matches) / total : 1.0;
}

/* ------------------------------------------------------------------ */
/* answers.py                                                          */
/* ------------------------------------------------------------------ */

export function answerLangFor(lang) {
  return ANSWER_LANGS.includes(lang) ? lang : 'english';
}

// answers._normalize: lowercase, split on whitespace, alias lookup per token.
function normalizeAnswers(text) {
  const tokens = (text || '').toLowerCase().split(/\s+/).filter(Boolean);
  return tokens.map((tok) => ALIASES[tok] || tok).join(' ');
}

function entryForTopic(topic) {
  return ANSWERS.find((entry) => entry.topic === topic) || null;
}

function textFor(answers, bank) {
  // Answers dicts may omit a language; fall back to English, never crash.
  if (answers !== null && typeof answers === 'object') {
    return answers[bank] || answers.english || Object.values(answers)[0] || '';
  }
  return answers || '';
}

export function topicMeta(topic) {
  const entry = entryForTopic(topic);
  if (entry === null) return { category: '', difficulty: '' };
  if ('category' in entry) {
    return { category: entry.category, difficulty: entry.difficulty || '' };
  }
  const [cat, diff] = TOPIC_META[topic] || ['', ''];
  return { category: cat, difficulty: diff };
}

// answers._clean_tokens: strip punctuation, then quotes, from both ends.
function cleanTokensAnswers(text) {
  const out = [];
  for (const raw of (text || '').toLowerCase().split(/\s+/)) {
    let tok = raw.replace(/^[.,?!:;()[\]{}<>]+/, '').replace(/[.,?!:;()[\]{}<>]+$/, '');
    tok = tok.replace(/^'+/, '').replace(/'+$/, '');
    tok = tok.replace(/^"+/, '').replace(/"+$/, '');
    if (tok) out.push(tok);
  }
  return out;
}

function scoreEntry(entry, raw, norm) {
  const rawLow = (raw || '').toLowerCase();
  let bestKw = 0.0;
  for (const kw of entry.keywords) {
    const k = kw.toLowerCase();
    if (norm.includes(k) || rawLow.includes(k)) {
      bestKw = Math.max(bestKw, 12.0 + cplen(k) / 4.0);
    } else {
      const kwTokens = cleanTokensAnswers(k);
      if (kwTokens.length && kwTokens.every((t) => norm.includes(t) || rawLow.includes(t))) {
        bestKw = Math.max(bestKw, 6.0);
      }
    }
  }
  const topicTokens = cleanTokensAnswers(entry.topic).filter(
    (t) => !STOPWORDS_ANSWERS.has(t) && cplen(t) > 2,
  );
  const queryTokens = new Set([...cleanTokensAnswers(norm), ...cleanTokensAnswers(rawLow)]);
  const overlap = topicTokens.filter((t) => queryTokens.has(t)).length;
  let fuzzy = 0.0;
  if (overlap) {
    const ratio = sequenceMatcherRatio(cleanTokensAnswers(norm).join(' '), entry.topic.toLowerCase());
    if (ratio >= 0.55) fuzzy = ratio * 6.0;
  }
  return bestKw + Math.min(overlap, 3) * 3.0 + fuzzy;
}

function topicsInCategory(category, limit = 4, exclude = null) {
  return topicList()
    .filter((t) => t.category === category && t.topic !== exclude)
    .map((t) => t.topic)
    .slice(0, limit);
}

export function answerQuery(transcript, lang = 'hinglish') {
  const bank = answerLangFor(lang);
  const norm = normalizeAnswers(transcript);
  const scored = ANSWERS.map((entry) => [scoreEntry(entry, transcript, norm), entry]);
  scored.sort((a, b) => b[0] - a[0]); // stable: ties keep bank order, like Python
  const [bestScore, bestEntry] = scored.length ? scored[0] : [0.0, null];
  if (bestEntry !== null && bestScore >= MATCH_THRESHOLD) {
    const meta = topicMeta(bestEntry.topic);
    return {
      topic: bestEntry.topic,
      answer: textFor(bestEntry.answers, bank),
      category: meta.category,
      difficulty: meta.difficulty,
      matched: true,
      family: null,
      suggestions: topicsInCategory(meta.category, 4, bestEntry.topic),
    };
  }
  // Family fallback: teach the pattern family instead of dead-ending.
  const normLow = norm.toLowerCase();
  const rawLow = (transcript || '').toLowerCase();
  let bestFamily = null;
  let bestFamilyScore = 0;
  for (const fam of FAMILY_GUIDES) {
    const hits = fam.keywords
      .filter((kw) => normLow.includes(kw) || rawLow.includes(kw))
      .reduce((sum, kw) => sum + cplen(kw), 0);
    if (hits > bestFamilyScore) {
      bestFamilyScore = hits;
      bestFamily = fam;
    }
  }
  if (bestFamily !== null && bestFamilyScore > 0) {
    return {
      topic: bestFamily.title,
      answer: textFor(bestFamily.answers, bank),
      category: 'Pattern family',
      difficulty: '',
      matched: false,
      family: bestFamily.id,
      suggestions: topicsInCategory(FAMILY_CATEGORIES[bestFamily.id] || '', 4),
    };
  }
  return {
    topic: 'Not in list',
    answer: FALLBACKS[bank],
    category: '',
    difficulty: '',
    matched: false,
    family: null,
    suggestions: suggestTopics('', 6).map((s) => s.topic),
  };
}

export function findAnswer(transcript, lang = 'hinglish') {
  const result = answerQuery(transcript, lang);
  return [result.topic, result.answer];
}

export function findFollowup(topic, kind, lang = 'hinglish') {
  const entry = entryForTopic(topic);
  const bank = answerLangFor(lang);
  if (entry === null) return FALLBACKS[bank];
  if (kind === 'example') {
    const ex = entry.example;
    return ex !== null && typeof ex === 'object' ? textFor(ex, bank) : ex;
  }
  return textFor(entry.simple, bank);
}

export function topics() {
  return ANSWERS.map((e) => e.topic);
}

export function topicList() {
  return ANSWERS.map((entry) => {
    const meta = topicMeta(entry.topic);
    return { topic: entry.topic, category: meta.category, difficulty: meta.difficulty };
  });
}

export function suggestTopics(query, limit = 6, exclude = null) {
  if (!((query || '').trim())) {
    const names = POPULAR.filter((t) => t !== exclude).slice(0, limit);
    return names
      .filter((t) => entryForTopic(t))
      .map((t) => ({ topic: t, ...topicMeta(t) }));
  }
  const norm = normalizeAnswers(query);
  const scored = ANSWERS.map((entry) => [scoreEntry(entry, query, norm), entry]);
  scored.sort((a, b) => b[0] - a[0]);
  const out = [];
  for (const [score, entry] of scored) {
    if (score <= 0 || entry.topic === exclude) continue;
    const meta = topicMeta(entry.topic);
    out.push({ topic: entry.topic, category: meta.category, difficulty: meta.difficulty });
    if (out.length >= limit) break;
  }
  if (!out.length) {
    const names = POPULAR.filter((t) => t !== exclude).slice(0, limit);
    return names
      .filter((t) => entryForTopic(t))
      .map((t) => ({ topic: t, ...topicMeta(t) }));
  }
  return out;
}

/* ------------------------------------------------------------------ */
/* approaches.py                                                       */
/* ------------------------------------------------------------------ */

// approaches._normalize: Python re [^\w\s] with Unicode \w (letters,
// numbers, underscore; combining marks are NOT word chars), then
// collapse whitespace and trim.
function normalizeApproaches(text) {
  return (text || '')
    .toLowerCase()
    .replace(/[^\p{L}\p{N}_\s]/gu, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function cleanTokensApproaches(text) {
  return normalizeApproaches(text).split(/\s+/).filter(Boolean);
}

function scoreAlgorithm(entry, raw, norm) {
  const rawLow = (raw || '').toLowerCase();
  let bestKw = 0.0;
  for (const kw of entry.aliases) {
    const k = kw.toLowerCase();
    if (norm.includes(k) || rawLow.includes(k)) {
      bestKw = Math.max(bestKw, 12.0 + cplen(k) / 4.0);
    } else {
      const kwTokens = cleanTokensApproaches(k);
      if (kwTokens.length && kwTokens.every((t) => norm.includes(t) || rawLow.includes(t))) {
        bestKw = Math.max(bestKw, 6.0);
      }
    }
  }
  const nameTokens = cleanTokensApproaches(entry.name).filter(
    (t) => !STOPWORDS_APPROACHES.has(t) && cplen(t) > 2,
  );
  const queryTokens = new Set([...cleanTokensApproaches(norm), ...cleanTokensApproaches(rawLow)]);
  const overlap = nameTokens.filter((t) => queryTokens.has(t)).length;
  let fuzzy = 0.0;
  if (overlap) {
    const ratio = sequenceMatcherRatio(cleanTokensApproaches(norm).join(' '), entry.name.toLowerCase());
    if (ratio >= 0.55) fuzzy = ratio * 6.0;
  }
  return bestKw + Math.min(overlap, 3) * 3.0 + fuzzy;
}

export function findAlgorithm(question) {
  const norm = normalizeApproaches(question);
  const scored = ALGORITHMS.map((entry) => [scoreAlgorithm(entry, question, norm), entry]);
  scored.sort((a, b) => b[0] - a[0]);
  const [bestScore, bestEntry] = scored.length ? scored[0] : [0.0, null];
  if (bestEntry !== null && bestScore >= MATCH_THRESHOLD) return bestEntry;
  return null;
}

export function suggestAlgorithms(query, limit = 6) {
  const popular = ['Prime Number Check', 'Two Sum', 'Binary Search', 'Quick Sort', 'Reverse Linked List', 'Breadth-First Search (BFS)'];
  const byName = new Map(ALGORITHMS.map((e) => [e.name, e]));
  const norm = normalizeApproaches(query);
  if (!norm) {
    return popular
      .slice(0, limit)
      .filter((n) => byName.has(n))
      .map((n) => ({ name: n, category: byName.get(n).category }));
  }
  const queryTokens = cleanTokensApproaches(norm);
  const scored = [];
  for (const entry of ALGORITHMS) {
    let score = scoreAlgorithm(entry, query, norm);
    if (cplen(norm) >= 2) {
      const haystacks = [entry.name.toLowerCase(), ...entry.aliases.map((a) => a.toLowerCase())];
      for (const hay of haystacks) {
        for (const tok of hay.split(/\s+/).filter(Boolean)) {
          if (queryTokens.some((q) => cplen(q) >= 2 && tok.startsWith(q))) {
            score += 4.0;
            break;
          }
        }
      }
    }
    scored.push([score, entry]);
  }
  scored.sort((a, b) => b[0] - a[0]);
  const out = [];
  for (const [score, entry] of scored) {
    if (score <= 0) continue;
    out.push({ name: entry.name, category: entry.category });
    if (out.length >= limit) break;
  }
  if (!out.length) {
    return popular
      .slice(0, limit)
      .filter((n) => byName.has(n))
      .map((n) => ({ name: n, category: byName.get(n).category }));
  }
  return out;
}

export function optimalApproach(entry) {
  return entry.approaches.find((a) => a.optimal) || null;
}

// Exported for parity testing.
export const _internals = {
  sequenceMatcherRatio,
  normalizeAnswers,
  normalizeApproaches,
  cleanTokensAnswers,
  cleanTokensApproaches,
  scoreEntry,
  scoreAlgorithm,
};
