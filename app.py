"""Bolke Seekho — a multilingual voice DSA revision buddy (Nov 16, 2026 rebuild).

Ask a DSA question by voice in any of 10 Indian languages (Gnani Prisma
speech-to-text), hear a pattern-style answer spoken back (Gnani Timbre
text-to-speech). 40 topics across arrays, strings, linked lists, stacks,
trees, graphs, dynamic programming, sorting, and heaps. The whole screen
translates when the language changes, and typed questions work even
without an API key (text answers only; voice needs the key).

Set GNANI_API_KEY (from app.gnani.ai) in the environment or in a .env file.
Run:  python app.py   then open http://127.0.0.1:5000
"""

import base64
import os
import tempfile

from flask import Flask, jsonify, render_template, request

from answers import LANGUAGES, answer_query, find_followup, suggest_topics, topic_list

app = Flask(__name__)

CATEGORY_ORDER = [
    "Arrays & Searching",
    "Strings & Hashing",
    "Linked List",
    "Stack & Queue",
    "Trees",
    "Graphs",
    "Dynamic Programming",
    "Sorting",
    "Heap",
]


def _load_dotenv():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


_load_dotenv()
API_KEY = os.environ.get("GNANI_API_KEY", "").strip()
TTS_VOICE = os.environ.get("BOLKE_TTS_VOICE", "Nalini").strip() or "Nalini"

# Timbre language parameter per answer language ("auto" lets it detect
# from the text; Roman Hinglish works best as auto).
TTS_LANG = {
    "hinglish": "auto",
    "english": "en-IN",
    "telugu": "te-IN",
    "tamil": "ta-IN",
    "kannada": "kn-IN",
    "malayalam": "ml-IN",
}


def _bank_lang(lang: str) -> str:
    from answers import answer_lang_for

    return answer_lang_for(lang if lang in LANGUAGES else "hinglish")


def transcribe(audio_bytes: bytes, lang: str) -> str:
    """Gnani Prisma (speech-to-text) in the chosen language."""
    from gnani.stt import GnaniSTTClient

    client = GnaniSTTClient(api_key=API_KEY)
    language_code = LANGUAGES.get(lang, "hi-IN")
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    try:
        result = client.transcribe(tmp_path, language_code=language_code)
    finally:
        os.unlink(tmp_path)
    if isinstance(result, dict):
        return result.get("transcript", "") or ""
    return getattr(result, "text", "") or ""


def speak(text: str, lang: str) -> bytes:
    """Gnani Timbre v2.5 (text-to-speech) in the answer's language, MP3 out."""
    from gnani.tts import AudioConfig, GnaniTTSClient

    bank = _bank_lang(lang)
    client = GnaniTTSClient(api_key=API_KEY)
    audio = client.synthesize(
        text,
        voice=TTS_VOICE,
        model="timbre-v2.5",
        language=TTS_LANG.get(bank, "auto"),
        audio_config=AudioConfig(container="mp3", sample_rate=48000, bitrate="128k"),
    )
    return audio


def spoken_payload(text: str, lang: str, topic: str = "") -> dict:
    """Text answer plus spoken audio when a key is set.

    Without a key, the text answer still works and voice_available is
    False, so the search bar never looks dead just because voice is off.
    """
    if not API_KEY:
        return {"topic": topic, "answer": text, "audio_base64": "", "tts_error": "", "voice_available": False}
    try:
        audio_b64 = base64.b64encode(speak(text, lang)).decode("ascii")
    except Exception as exc:  # keep the text answer usable even if TTS fails
        return {
            "topic": topic,
            "answer": text,
            "audio_base64": "",
            "tts_error": f"{type(exc).__name__}: {exc}",
            "voice_available": False,
        }
    return {"topic": topic, "answer": text, "audio_base64": audio_b64, "tts_error": "", "voice_available": True}


@app.get("/")
def home():
    topics = topic_list()
    categories = [c for c in CATEGORY_ORDER if any(t["category"] == c for t in topics)]
    return render_template(
        "index.html",
        topics=topics,
        categories=categories,
        key_set=bool(API_KEY),
        languages=list(LANGUAGES.keys()),
    )


@app.get("/api/topics")
def list_topics():
    topics = topic_list()
    return jsonify({"topics": topics, "count": len(topics)})


@app.get("/api/suggest")
def suggest():
    query = (request.args.get("q") or "").strip()
    try:
        limit = int(request.args.get("limit") or 6)
    except ValueError:
        limit = 6
    limit = max(1, min(limit, 10))
    return jsonify({"suggestions": suggest_topics(query, limit=limit)})


@app.post("/api/ask")
def ask_voice():
    if not API_KEY:
        return (
            jsonify(
                {
                    "error": "Voice needs a Gnani API key. Add GNANI_API_KEY to the .env file and restart — typed questions work without it.",
                    "error_code": "NO_API_KEY",
                }
            ),
            400,
        )
    lang = (request.form.get("lang") or "hinglish").lower()
    file = request.files.get("audio")
    if file is None:
        return jsonify({"error": "No audio received.", "error_code": "NO_AUDIO"}), 400
    audio_bytes = file.read()
    if not audio_bytes:
        return jsonify({"error": "Empty recording. Hold the mic button, speak, then tap again to stop.", "error_code": "EMPTY_AUDIO"}), 400
    try:
        transcript = transcribe(audio_bytes, lang)
    except Exception as exc:
        return jsonify({"error": f"Speech-to-text failed: {type(exc).__name__}: {exc}", "error_code": "STT_FAILED"}), 502
    if not transcript.strip():
        return (
            jsonify(
                {
                    "error": "Prisma returned an empty transcript. Try speaking again, closer to the mic, or type the question instead.",
                    "error_code": "EMPTY_TRANSCRIPT",
                }
            ),
            422,
        )
    result = answer_query(transcript, lang)
    payload = spoken_payload(result["answer"], lang, result["topic"])
    payload.update(
        {
            "transcript": transcript,
            "category": result["category"],
            "difficulty": result["difficulty"],
            "matched": result["matched"],
            "family": result["family"],
            "suggestions": result["suggestions"],
            "answer_lang": _bank_lang(lang),
        }
    )
    return jsonify(payload)


@app.post("/api/text")
def ask_text():
    """Typed-question search. Works without an API key (text only)."""
    data = request.get_json(force=True, silent=True) or {}
    question = (data.get("question") or "").strip()
    lang = (data.get("lang") or "hinglish").lower()
    if not question:
        return jsonify({"error": "Type or pick a question first.", "error_code": "EMPTY_QUESTION"}), 400
    result = answer_query(question, lang)
    payload = spoken_payload(result["answer"], lang, result["topic"])
    payload.update(
        {
            "transcript": question,
            "category": result["category"],
            "difficulty": result["difficulty"],
            "matched": result["matched"],
            "family": result["family"],
            "suggestions": result["suggestions"],
            "answer_lang": _bank_lang(lang),
        }
    )
    return jsonify(payload)


@app.post("/api/followup")
def followup():
    """Clarifying follow-ups after an answer: 'simple' or 'example'."""
    data = request.get_json(force=True, silent=True) or {}
    topic = (data.get("topic") or "").strip()
    kind = (data.get("kind") or "simple").strip()
    lang = (data.get("lang") or "hinglish").lower()
    if not topic:
        return jsonify({"error": "No topic to clarify.", "error_code": "NO_TOPIC"}), 400
    if kind not in ("simple", "example"):
        kind = "simple"
    text = find_followup(topic, kind, lang)
    payload = spoken_payload(text, lang, topic)
    payload.update({"kind": kind, "answer_lang": _bank_lang(lang)})
    return jsonify(payload)


@app.errorhandler(404)
def api_not_found(err):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Unknown API route.", "error_code": "NOT_FOUND"}), 404
    return err


@app.errorhandler(405)
def api_method_not_allowed(err):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Wrong method for this API route.", "error_code": "METHOD_NOT_ALLOWED"}), 405
    return err


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
