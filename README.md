# Bolke Seekho — Voice DSA Revision in Your Language 🎙️

India has 700+ living languages, and most DSA teaching happens in English or Hindi.
Bolke Seekho lets a student **ask a DSA question by voice in their own language** and
hear the answer spoken back — the way they would actually revise with a friend.

Built for the **Gnani AI Great Indian AI Internship Challenge** (submitted Nov 15, 2026)
and **rebuilt on Nov 16, 2026** from real testing feedback: a livelier interface, full
interface translation, much wider DSA coverage, and a search bar that actually works.
Open-ended LLM answers were added the same night, so the app is not limited to its
topic list — any DSA question gets an answer.

- **Ask in 10 Indian languages** (Gnani **Prisma** speech-to-text): Hinglish, English,
  Telugu, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi — including
  natural code-switching, because tech terms stay English in every language.
- **Answers spoken back** (Gnani **Timbre v2.5**) in **Hinglish, English, Telugu,
  Tamil, Kannada and Malayalam** (Marathi/Bengali/Gujarati/Punjabi questions are
  understood and answered in English for now).
- **The whole screen translates** when the language changes: headings, buttons, hints,
  banners, and status messages — not just the voice. Topic and category names stay in
  English, as students actually say them ("linked list", "DP", "binary search").
- **AI-era answers, not code recitation:** every answer teaches the *pattern* — why it
  works, its complexity, and the trade-off to state in an interview.
- **40 topics**, browsable by category, with live search suggestions as you type.
  Questions outside the list get a **pattern-family guide** (e.g. graph patterns,
  DP patterns) instead of a dead end, plus "try next" suggestions.
- **Any DSA question:** with an LLM configured (see below), questions outside the
  40 topics are answered by the model in the same pattern style and in the
  student's language, and labelled "AI answer" in the chat. Without an LLM, the
  pattern-family guides above apply instead.
- **Clarify, don't dead-end:** after any answer, tap **"Explain simpler"** for a
  simpler version or **"Give an example"** for a worked example. Answers can be
  replayed or copied, and explored topics are tracked on screen.
- **Search works without an API key:** typed questions always return text answers.
  Voice (listening + spoken replies) needs a Gnani API key.

## Topics (40)

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

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env        # paste your Gnani API key (from app.gnani.ai) into .env
python app.py               # open http://127.0.0.1:5000
```

Pick your language, tap the mic, and ask — e.g. *"టూ సమ్ ఎలా చేయాలి?"* or
*"Two sum array mein kaise karte hain?"* — then listen to the answer, ask for it
simpler, or ask for an example. Or type in the search bar and press **Ask**
(or Enter), pick a suggestion, or tap any topic card.

Without a key, the app still runs: search, browsing, and text answers work, and a
banner explains how to turn voice on. Voice needs the key for both Prisma and Timbre.

## Answering any DSA question (LLM fallback)

The 40 topics above are the curated, checked bank — fast and reliable. For
everything else, the app asks a language model, so a student is never stuck
with "pick a topic from the list". Any **OpenAI-compatible chat API** works.
Add these three lines to `.env` (see `.env.example`):

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
  Cloud use spends your provider credits/quotas; the bank questions never
  call the LLM, so only genuinely new questions cost anything.
- **Off:** leave the three lines empty and the app behaves as before — bank
  answers plus pattern-family guides. If the LLM is unreachable or errors,
  the app silently falls back to the family guide instead of breaking.
- **Trust:** LLM answers are labelled "AI answer" in the chat. They follow
  the same pattern → why → complexity → trade-off style, but they are
  generated, so verify anything surprising before an interview. The model is
  instructed to answer DSA questions only.

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
- **"I could not catch that" / family guide:** the question did not match one topic
  and no LLM is configured (or it failed). Try the topic name itself (e.g. "BFS",
  "quick sort"), tap a topic card, or configure the LLM fallback above.
- **LLM answers never appear:** check the three `BOLKE_LLM_*` lines in `.env`
  (base URL, model, key if your provider needs one), then restart
  `python app.py` — `.env` is read at startup. A wrong base URL or model name
  fails silently back to family guides (the app never logs the key or the
  error), so double-check the three values and restart.
- **Wrong GitHub account:** if the repo is missing in the browser, check which
  username is signed in at github.com — the repo is under `Midhil-6473`.

## How it works

Browser mic → 16 kHz WAV → **Prisma** (STT, chosen language) → transcript normalised
(tolerant of native-script and misheard forms) → scored topic match (keyword phrases,
token overlap, fuzzy topic-name similarity) → curated, pattern-style answer bank →
**Timbre v2.5** (TTS, answer's language) → spoken reply.

Unmatched questions go to the configured LLM (`llm.py`, any OpenAI-compatible
chat API) with a system prompt enforcing the same pattern style and the
student's language; if no LLM is configured or it fails, they fall back to a
pattern-family guide when the question names a family (trees, graphs, DP,
sorting, heaps, ...), otherwise to a short message that points at the topic
browser.

API: `GET /` (page), `GET /api/topics`, `GET /api/suggest?q=...`,
`POST /api/ask` (voice, needs key), `POST /api/text` (typed, works without a key),
`POST /api/followup` (simple/example, works without a key for text). Answer
payloads carry an `llm` boolean: true when the answer came from the model.

## Files

- `app.py` — Flask server, Gnani Prisma/Timbre wiring, API routes.
- `llm.py` — open-ended answers via any OpenAI-compatible chat API (stdlib only).
- `answers.py` — original 12 topics, matching, family guides, fallbacks.
- `topics_extra.py` — 28 more topics added in the Nov 16, 2026 rebuild.
- `templates/index.html` — the whole interface, including its 10-language UI text.
- `requirements.txt` — `flask`, `gnani-vachana`.

Tags: Prisma v2.5 (STT) · Timbre v2.5 (TTS).
