# Bolke Seekho — Voice DSA Revision in Your Language 🎙️

India has 700+ living languages, and most DSA teaching happens in English or Hindi.
Bolke Seekho lets a student **ask a DSA question by voice in their own language** and
hear the answer spoken back — the way they would actually revise with a friend.

Built for the **Gnani AI Great Indian AI Internship Challenge** (submitted Nov 15, 2026)
and **rebuilt on Nov 16, 2026** from real testing feedback: a livelier interface, full
interface translation, much wider DSA coverage, and a search bar that actually works.

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
- **"I could not catch that" / family guide:** the question did not match one topic.
  Try the topic name itself (e.g. "BFS", "quick sort"), or tap a topic card.
- **Wrong GitHub account:** if the repo is missing in the browser, check which
  username is signed in at github.com — the repo is under `Midhil-6473`.

## How it works

Browser mic → 16 kHz WAV → **Prisma** (STT, chosen language) → transcript normalised
(tolerant of native-script and misheard forms) → scored topic match (keyword phrases,
token overlap, fuzzy topic-name similarity) → curated, pattern-style answer bank →
**Timbre v2.5** (TTS, answer's language) → spoken reply.

Unmatched questions fall back to a pattern-family guide when the question names a
family (trees, graphs, DP, sorting, heaps, ...), otherwise to a short message that
points at the topic browser.

API: `GET /` (page), `GET /api/topics`, `GET /api/suggest?q=...`,
`POST /api/ask` (voice, needs key), `POST /api/text` (typed, works without a key),
`POST /api/followup` (simple/example, works without a key for text).

## Files

- `app.py` — Flask server, Gnani Prisma/Timbre wiring, API routes.
- `answers.py` — original 12 topics, matching, family guides, fallbacks.
- `topics_extra.py` — 28 more topics added in the Nov 16, 2026 rebuild.
- `templates/index.html` — the whole interface, including its 10-language UI text.
- `requirements.txt` — `flask`, `gnani-vachana`.

Tags: Prisma v2.5 (STT) · Timbre v2.5 (TTS).
