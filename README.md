# Bolke Seekho — Search Any DSA Algorithm, Learn Every Way to Solve It 🎙️

India has 700+ living languages, and most DSA teaching happens in English or Hindi.
Bolke Seekho lets a student **search any algorithm** — by typing or by voice in their
own language — and see the **key code first**, then **every approach** with its logic,
code, and time/space complexity, with the **best technique flagged**. Then they can
**ask follow-up questions** about the algorithm or one of its methods, and the voice
agent answers in that context.

Built for the **Gnani AI Great Indian AI Internship Challenge** (submitted Nov 15, 2026),
rebuilt Nov 16, 2026 from real testing feedback (full interface translation, wider
coverage, working search, open-ended LLM answers), redesigned again on
Nov 17, 2026 as a search-first interface, and given a full **voice-first revision
studio** redesign the same night: a calm dark interface, a 3D Learning Orb that
shows voice state, a conversation drawer for follow-ups, and a voice sheet that
covers every voice state gracefully.

- **Clean search-first interface:** one search bar (plus mic) under a Learning Orb.
  No stacked lists, no catalogue, no dashboard. Type or say an algorithm name —
  "prime number", "quicksort", "BFS" — and the answer appears. Press `/` to jump
  to search from anywhere.
- **Key code first, then all approaches:** every result shows the main code of the
  best approach up front, then each approach with its key logic, Java code, and
  time/space complexity. The optimal technique carries a **Best** badge, with the
  reasoning in its logic text (e.g. prime checking: trial division, √n trial
  division, 6k±1 optimized, and the Sieve for ranges). Desktop gets an approach
  navigator; mobile gets accordions with the best approach open by default.
- **Ask about a method:** every approach has an **"Ask about this method"** button
  that opens a conversation drawer (desktop) or bottom sheet (mobile) showing the
  context explicitly ("Prime Number Check → 6k ± 1 optimised"). Questions go to
  the voice agent with the algorithm and method as context, so answers stay on
  the method the student is looking at. Voice questions get spoken answers;
  typed questions get text answers with Listen, pause, replay, and transcript.
  The algorithm page stays underneath, so nobody loses their place.
- **Voice states, handled honestly:** a voice sheet covers permission request,
  listening (with amplitude ripples and a live timer), processing, speaking,
  paused playback, no speech detected, permission denied, voice not configured,
  and unsupported browsers — always with a text-input fallback. Every spoken
  answer also appears as readable text. Spoken-answer support per language is
  configuration-driven; the four languages without spoken answers yet are
  understood and answered in English, and the interface says so politely.
- **Ask in 10 Indian languages** (Gnani **Prisma** speech-to-text): Hinglish, English,
  Telugu, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi — including
  natural code-switching, because tech terms stay English in every language.
- **Answers spoken back** (Gnani **Timbre v2.5**) in **Hinglish, English, Telugu,
  Tamil, Kannada and Malayalam** (Marathi/Bengali/Gujarati/Punjabi questions are
  understood and answered in English for now).
- **The whole screen translates** when the language changes: headings, buttons, hints,
  banners, and status messages — not just the voice. Algorithm and approach names
  stay in English, as students actually say them ("linked list", "DP", "binary search").
  UI text lives in one 110-key table per language in `templates/index.html`.
- **Design tokens** (CSS custom properties in `templates/index.html`): background
  `#070A12`, surface `#0D1320`, elevated `#141C2D`, text `#F5F7FB` / `#9AA7BC`,
  brand violet `#8B7CFF`, warm voice accent `#FFB86B`, Best accent `#43D9C3`,
  error `#FF7B86`, borders at white 8–10% opacity. Manrope + Noto Sans script
  families for UI text, JetBrains Mono for code. A light theme is included
  (settings popover). The orb is inline SVG with CSS state animations and a
  static fallback under `prefers-reduced-motion`. Touch targets are 44 px or
  larger, focus states are visible, and state is never carried by colour alone.
- **AI-era teaching, not code recitation:** every approach explains the *key logic* —
  why it works — plus its complexity and trade-off, so the student can state it in
  an interview.
- **41 curated algorithms** with hand-written approaches and Java code (see below).
  Anything else is answered by a configured LLM **in the same shape** — key code,
  approaches, complexities, best pick — and labelled "AI answer". Without an LLM,
  unmatched searches fall back to a pattern-family guide instead of a dead end.
- **Search works without an API key:** typed searches and text answers always work.
  Voice (listening + spoken replies) needs a Gnani API key.

## Algorithms (41)

- **Arrays & Searching:** Two Sum, 3Sum, Container With Most Water, Best Time to Buy
  and Sell Stock, Product of Array Except Self, Longest Consecutive Sequence,
  Subarray Sum Equals K (Prefix Sum), Remove Duplicates from Sorted Array,
  Move Zeroes, Sliding Window, Binary Search, Merge Intervals,
  Trapping Rain Water, Maximum Subarray (Kadane's Algorithm)
- **Strings & Hashing:** Longest Substring Without Repeating Characters,
  Valid Anagram, Group Anagrams, Longest Palindromic Substring
- **Linked List:** Reverse Linked List, Linked List Cycle, Merge Two Sorted Lists,
  Remove Nth Node From End of List
- **Stack & Queue:** Valid Parentheses, Min Stack, Next Greater Element
- **Trees:** Binary Tree Traversals, Maximum Depth of Binary Tree, Invert Binary Tree,
  Validate Binary Search Tree, Lowest Common Ancestor of a BST
- **Graphs:** Breadth-First Search (BFS), Depth-First Search (DFS), Number of Islands
- **Dynamic Programming:** Climbing Stairs, House Robber, Coin Change
- **Sorting:** Quick Sort, Merge Sort
- **Heap:** Kth Largest Element, Top K Frequent Elements
- **Math & Number Theory:** Prime Number Check (trial division, √n, 6k±1, Sieve)

Code snippets are the core Java methods (assume `import java.util.*;`), not full
programs — the key code, as the interface promises.

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env        # paste your Gnani API key (from app.gnani.ai) into .env
python app.py               # open http://127.0.0.1:5000
```

Pick your language, search for an algorithm — e.g. *"prime number"* or *"quicksort"* —
read the key code and the approaches, then ask a follow-up: tap **"Ask about this
method"** on any approach, or type/speak a question in the "Ask about this
algorithm" box. Or tap the mic and ask by voice — e.g. *"టూ సమ్ ఎలా చేయాలి?"*.

Without a key, the app still runs: search, approaches, and text answers work, and a
banner explains how to turn voice on. Voice needs the key for both Prisma and Timbre.

## Answering any DSA question (LLM fallback)

The 41 algorithms above are the curated, checked bank — fast and reliable. For
everything else, the app asks a language model for the same structured shape
(key logic, approaches with Java code and complexities, one best pick), and
follow-up questions are answered with the on-screen algorithm as context. Any
**OpenAI-compatible chat API** works. Add these three lines to `.env`
(see `.env.example`):

```
BOLKE_LLM_BASE_URL=http://localhost:11434/v1
BOLKE_LLM_MODEL=qwen2.5:3b
BOLKE_LLM_API_KEY=
```

- **Local and free:** install Ollama on the laptop, pull a small model
  (`ollama pull qwen2.5:3b`), and use the base URL above with no key. The
  first answer can be slow while the model loads; quality depends on the
  model you pick — small local models explain well but can get details wrong.
- **Cloud:** use your provider's OpenAI-compatible base URL, model name, and
  API key (Ollama Cloud, Groq, OpenRouter, Gemini's OpenAI-compatible
  endpoint, and similar). Confirm the exact base URL and model name in your
  provider's docs — they change, and this README does not hard-code them.
  Cloud use spends your provider credits/quotas; bank questions never
  call the LLM, so only genuinely new questions cost anything.
- **Off:** leave the three lines empty and the app behaves as before — bank
  answers plus pattern-family guides, and follow-ups fall back to the bank's
  spoken answer for the algorithm. If the LLM is unreachable or errors, the
  app silently falls back instead of breaking.
- **Trust:** LLM answers are labelled "AI answer". They follow the same
  key-logic → approaches → best-pick shape, but they are generated, so verify
  anything surprising before an interview. The model is instructed to answer
  DSA questions only, and to return structured JSON for searches.

## Troubleshooting

- **"Unable to connect" / "Could not reach the app server":** the server is not
  running. In a terminal inside this folder, run `python app.py` and keep that
  terminal open, then refresh the browser.
- **Search does nothing:** press the **Ask** button or Enter. If an error box appears,
  it says what went wrong (no server, no key for voice, empty recording, ...).
- **Voice says the key is missing:** create `.env` next to `app.py` with the single
  line `GNANI_API_KEY=<your key>`, no spaces or quotes. Beware Notepad saving it as
  `.env.txt` — the file must be named exactly `.env`. Restart `python app.py`.
- **Mic blocked:** allow microphone permission in the browser, or type the question.
- **A search shows a guide instead of approaches:** the question did not match one
  algorithm and no LLM is configured (or it failed). Try the algorithm name itself
  (e.g. "BFS", "quick sort", "prime"), or configure the LLM fallback above.
- **LLM answers never appear:** check the three `BOLKE_LLM_*` lines in `.env`
  (base URL, model, key if your provider needs one), then restart
  `python app.py` — `.env` is read at startup. A wrong base URL or model name
  fails silently back to family guides (the app never logs the key or the
  error), so double-check the three values and restart.
- **Wrong GitHub account:** if the repo is missing in the browser, check which
  username is signed in at github.com — the repo is under `Midhil-6473`.

## How it works

Search (typed) or voice (mic → 16 kHz WAV → **Prisma** STT) → transcript
normalised (tolerant of native-script and misheard forms) → scored algorithm
match (alias phrases, token overlap, fuzzy name similarity) over
`approaches.py` → key code + approaches + best pick rendered; the
**Timbre v2.5** spoken summary uses the pattern-style answer bank
(`answers.py`) when the algorithm has one.

Unmatched searches go to the configured LLM (`llm.py`, any OpenAI-compatible
chat API), first for the same structured JSON shape, then for a plain answer;
follow-up questions go to the LLM with the on-screen algorithm and approaches
as context. If no LLM is configured or it fails, searches fall back to a
pattern-family guide when the question names a family (trees, graphs, DP,
sorting, heaps, ...), otherwise to a short message; follow-ups fall back to
the bank's answer for the algorithm.

API: `GET /` (page), `GET /api/suggest?q=...`,
`POST /api/search` (typed, works without a key; responses include a `summary`
field — the spoken summary used by the header Listen button),
`POST /api/ask` (voice, needs key; accepts `algorithm`/`approach`/`approaches`
for contextual follow-ups), `POST /api/followup` (question about the
algorithm on screen), `POST /api/speak` (text to speech, needs key).
Algorithm payloads carry `kind: "algorithm"`, `source` (`bank`/`llm`), and an
`llm` boolean: true when the content came from the model.

## Files

- `app.py` — Flask server, Gnani Prisma/Timbre wiring, API routes.
- `approaches.py` — 41 algorithms: key logic, approaches, Java key code, complexities, best pick, matching.
- `llm.py` — open-ended structured answers and contextual follow-ups via any OpenAI-compatible chat API (stdlib only).
- `answers.py` — spoken pattern-style answer bank (12 original topics), matching, family guides, fallbacks.
- `topics_extra.py` — 28 more spoken-answer topics added in the Nov 16, 2026 rebuild.
- `templates/index.html` — the whole interface: design tokens, Learning Orb, result
  views, conversation drawer, voice sheet, and 10-language UI text (110 keys).
- `requirements.txt` — `flask`, `gnani-vachana`.

Tags: Prisma v2.5 (STT) · Timbre v2.5 (TTS).
