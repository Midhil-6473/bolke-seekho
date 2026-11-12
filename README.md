# Bolke Seekho — Voice DSA Revision in Your Language 🎙️

India has 700+ living languages, and most DSA teaching happens in English or Hindi.
Bolke Seekho lets a student **ask a DSA question by voice in their own language** and
hear the answer spoken back — the way they would actually revise with a friend.

Built for the **Gnani AI Great Indian AI Internship Challenge** (submission deadline:
**Nov 10, 2026, 11:59 PM IST**).

- **Ask in 10 Indian languages** (Gnani **Prisma** speech-to-text): Hinglish, English,
  Telugu, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi — including
  natural code-switching, because tech terms stay English in every language.
- **Answers spoken back** (Gnani **Timbre v2.5**) with full answer banks in **Hinglish,
  English, Telugu, Tamil, Kannada and Malayalam** (Marathi/Bengali/Gujarati/Punjabi
  questions are understood and answered in English for now).
- **AI-era answers, not code recitation:** every answer teaches the *pattern* — why it
  works, its complexity, and the trade-off to state in an interview.
- **Clarify, don't dead-end:** after any answer, tap **"Aur simple mein samjhao"** for a
  simpler version or **"Ek example do"** for a worked example. If a question is not
  understood, the app asks a clarifying question instead of failing.

Covers 12 core topics: Two Sum, 3Sum, Container With Most Water, Best Time to Buy and
Sell Stock, Product of Array Except Self, Longest Consecutive Sequence, Prefix Sum
(Subarray Sum = K), Remove Duplicates, Move Zeroes, Longest Substring Without Repeating
Characters, Valid Anagram, Sliding Window.

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env        # paste your Gnani API key (from app.gnani.ai) into .env
python app.py               # open http://127.0.0.1:5000
```

Pick your language, tap the mic, and ask — e.g. *"టూ సమ్ ఎలా చేయాలి?"* or
*"Two sum array mein kaise karte hain?"* — then listen to the answer, ask for it
simpler, or ask for an example.

## How it works

Browser mic → 16 kHz WAV → **Prisma** (STT, chosen language) → transcript normalised
(tolerant of native-script and misheard forms) → topic matched to a curated,
pattern-style answer bank → **Timbre v2.5** (TTS, answer's language) → spoken reply.

Tags: Prisma v2.5 (STT) · Timbre v2.5 (TTS).
