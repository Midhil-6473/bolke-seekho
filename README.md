# Bolke Seekho — Voice DSA Revision (React + Node)

A voice-first DSA revision studio: ask any data structures or
algorithms question by typing or by voice, in your own language, and
get the key logic, the key code of the best approach, every approach
with Java code and time/space complexity, and the best technique
flagged — then ask follow-up questions about the algorithm or one of
its methods.

This is the React (Vite) + Node (Express) build. It is a behaviour-for-
behaviour rewrite of the original Flask + vanilla-JS app: same 41
curated algorithms, same answer banks, same matcher, same API, same
design, same 10-language UI (110 translated strings per language).

## How it works

- **Search-first UI.** One search bar and one mic — no catalogue, no
  stacked lists. Search shows Key Logic first, then the Key Code of the
  best approach, then All Approaches (desktop navigator, mobile
  accordions with the best open by default).
- **41 curated algorithms** with 2–4 approaches each, exactly one
  flagged Best, Java code, time/space chips — including Prime Number
  Check (trial division, √n, 6k ± 1 ★, Sieve).
- **Any DSA question.** Off-list searches go to a configured LLM, which
  answers in the same structured shape, labelled "AI answer". Without
  an LLM, pattern-family guides answer instead of a dead end.
- **Contextual follow-ups.** A conversation drawer keeps the algorithm
  (and optionally one method) in context; suggested questions included.
- **Voice.** Gnani Prisma speech-to-text + Timbre text-to-speech
  (voice Nalini) in 10 languages: 6 spoken (Hinglish, English, Telugu,
  Tamil, Kannada, Malayalam), 4 understood with English voice answers.
  Typed search works fully without an API key; voice needs one.
- **10-language UI.** The whole interface translates; algorithm and
  approach names stay in English. Light theme + voice-answers switch
  in settings.

## Run it

Requires Node.js 18+ (uses the global `fetch`).

```sh
npm install
npm run build     # build the React client once
npm start         # serves the app + API at http://127.0.0.1:5000
```

For development (hot reload + API proxy):

```sh
npm run dev       # Vite on http://127.0.0.1:5173, API on :5000
```

`npm run build` writes the client into `server/public/`; `npm start`
serves that build. Rebuild after changing anything under `client/`.

## Configuration (.env)

Copy `.env.example` to `.env` in the project root (the file the server
looks for). Never commit a real key.

```sh
GNANI_API_KEY=            # from app.gnani.ai — enables voice
BOLKE_TTS_VOICE=Nalini    # optional Timbre voice
BOLKE_LLM_BASE_URL=       # e.g. http://localhost:11434/v1 (Ollama)
BOLKE_LLM_MODEL=          # e.g. qwen2.5:3b
BOLKE_LLM_API_KEY=        # optional; omit for local servers without auth
```

- Without `GNANI_API_KEY`, typed search and follow-ups work; the mic
  shows a clear "voice not set up" state instead of failing silently.
- Without the `BOLKE_LLM_*` lines, off-list questions get pattern-family
  guides. Any OpenAI-compatible chat API works (Ollama locally is free).
- The LLM key is only ever sent to the configured base URL, as a Bearer
  header, and is never logged.

## API

| Route | Method | Body | Notes |
| --- | --- | --- | --- |
| `/api/config` | GET | — | `{key_set, languages}` for the client |
| `/api/suggest` | GET | `?q=&limit=` | Live search suggestions (limit 1–10, default 6) |
| `/api/search` | POST | `{question, lang}` | Algorithm or answer; works without a key |
| `/api/ask` | POST | multipart `audio` + `lang`, optional `algorithm`/`approach`/`approaches` | Voice search / voice follow-up; needs a key |
| `/api/followup` | POST | `{question, lang, algorithm, approach?, approaches?}` | Context-aware; legacy `{topic, kind}` form still honoured |
| `/api/speak` | POST | `{text, lang}` | Speak text aloud; needs a key |

Error responses are JSON `{error, error_code}` with the same messages
and HTTP statuses as the Flask build (`EMPTY_QUESTION`, `NO_API_KEY`,
`NO_AUDIO`, `EMPTY_AUDIO`, `STT_FAILED`, `EMPTY_TRANSCRIPT`,
`NO_TOPIC`, `NO_ALGORITHM`, `EMPTY_TEXT`, `NOT_FOUND`,
`METHOD_NOT_ALLOWED`).

## Project layout

```
client/                 React + Vite frontend
  index.html            page shell (fonts, title, #root)
  src/
    main.jsx            React entry point
    App.jsx             views, search, drawer, voice sheet, audio
    i18n.js             110 UI strings x 10 languages + LANG_META
    icons.jsx           Lucide-style inline SVG icons
    orb.jsx             the Learning Orb SVG
    highlight.js        lightweight Java syntax highlighter
    recorder.js         16 kHz mono WAV recorder for Prisma
    clipboard.js        copy helper with fallback
    index.css           design tokens + all styles
    components/
      SearchBox.jsx     search input + live suggestions + mic
      ResultView.jsx    algorithm / answer rendering, accordions, navigator
      Drawer.jsx        conversation drawer
      VoiceSheet.jsx    voice-sheet state machine (10 states + error)
server/
  src/
    server.js           Express app: routes, .env loading, static serving
    bank.js             matcher + lookup logic (port of answers.py /
                        topics_extra.py / approaches.py, including a
                        faithful difflib.SequenceMatcher port)
    bank-data.js        generated data: 40 answer-bank topics, 10 family
                        guides, 41 algorithms (aliases already include the
                        merged spoken-bank keywords, as at Python runtime)
    llm.js              OpenAI-compatible LLM client (port of llm.py)
    gnani.js            Gnani Prisma + Timbre REST calls, replicating the
                        gnani-vachana 0.10.0 SDK's wire behaviour
  public/               built client (generated by `npm run build`)
```

## Honest limits

- **Voice is untested live.** There is no Gnani API key in the build
  environment, so Prisma/Timbre calls have never run end to end from
  this codebase. The no-key error paths are verified, and the REST
  calls replicate the `gnani-vachana` 0.10.0 SDK's exact endpoints,
  headers and payloads (inspected from the installed package), but the
  mic flow needs a real key on a real machine to confirm.
- **Live LLM answering is untested.** The LLM client was verified
  against a mock OpenAI-compatible endpoint (structured answers,
  follow-ups with method focus, graceful degradation when unconfigured
  or failing). Model answers can be wrong — the UI labels them
  "AI answer"; verify before interviews.
- The Gnani contest submission used the earlier Flask build; this
  rewrite is a continuation of the same project, not a new submission.

## License

MIT — see LICENSE.
