"""Bolke Seekho — a multilingual voice DSA revision buddy.

Ask a DSA question by voice in any of 10 Indian languages (Gnani Prisma
speech-to-text), hear a pattern-style answer spoken back (Gnani Timbre
text-to-speech). Full answer banks: Hinglish, English, Telugu, Tamil,
Kannada, Malayalam; other languages are understood and answered in English.

Set GNANI_API_KEY (from app.gnani.ai) in the environment or in a .env file.
Run:  python app.py   then open http://127.0.0.1:5000
"""

import base64
import os
import tempfile

from flask import Flask, jsonify, render_template, request

from answers import LANGUAGES, find_answer, find_followup, topics

app = Flask(__name__)


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

# Timbre v2.5 voice per answer language (verified against the live API).
VOICE_BY_LANG = {
    "hinglish": "Nalini",
    "english": "Nalini",
    "telugu": "Nalini",
    "tamil": "Nalini",
    "kannada": "Nalini",
    "malayalam": "Nalini",
}

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
        voice=VOICE_BY_LANG.get(bank, "Nalini"),
        model="timbre-v2.5",
        language=TTS_LANG.get(bank, "auto"),
        audio_config=AudioConfig(container="mp3", sample_rate=48000, bitrate="128k"),
    )
    return audio


def spoken_payload(text: str, lang: str, topic: str = ""):
    audio_b64 = ""
    tts_error = ""
    try:
        audio_b64 = base64.b64encode(speak(text, lang)).decode("ascii")
    except Exception as exc:  # keep the text answer usable even if TTS fails
        tts_error = f"{type(exc).__name__}: {exc}"
    return {"topic": topic, "answer": text, "audio_base64": audio_b64, "tts_error": tts_error}


@app.get("/")
def home():
    return render_template("index.html", topics=topics(), key_set=bool(API_KEY), languages=list(LANGUAGES.keys()))


@app.post("/api/ask")
def ask_voice():
    if not API_KEY:
        return jsonify({"error": "GNANI_API_KEY is not set. Add it to .env and restart."}), 400
    lang = (request.form.get("lang") or "hinglish").lower()
    file = request.files.get("audio")
    if file is None:
        return jsonify({"error": "No audio received."}), 400
    audio_bytes = file.read()
    try:
        transcript = transcribe(audio_bytes, lang)
    except Exception as exc:
        return jsonify({"error": f"Speech-to-text failed: {type(exc).__name__}: {exc}"}), 502
    if not transcript.strip():
        return jsonify({"error": "Prisma returned an empty transcript. Try speaking again, closer to the mic."}), 422
    topic, answer_text = find_answer(transcript, lang)
    payload = spoken_payload(answer_text, lang, topic)
    payload["transcript"] = transcript
    return jsonify(payload)


@app.post("/api/text")
def ask_text():
    """Typed-question fallback (also handy if the mic is unavailable)."""
    if not API_KEY:
        return jsonify({"error": "GNANI_API_KEY is not set. Add it to .env and restart."}), 400
    data = request.get_json(force=True, silent=True) or {}
    question = (data.get("question") or "").strip()
    lang = (data.get("lang") or "hinglish").lower()
    if not question:
        return jsonify({"error": "Empty question."}), 400
    topic, answer_text = find_answer(question, lang)
    payload = spoken_payload(answer_text, lang, topic)
    payload["transcript"] = question
    return jsonify(payload)


@app.post("/api/followup")
def followup():
    """Clarifying follow-ups after an answer: 'simple' or 'example'."""
    if not API_KEY:
        return jsonify({"error": "GNANI_API_KEY is not set. Add it to .env and restart."}), 400
    data = request.get_json(force=True, silent=True) or {}
    topic = (data.get("topic") or "").strip()
    kind = (data.get("kind") or "simple").strip()
    lang = (data.get("lang") or "hinglish").lower()
    if not topic:
        return jsonify({"error": "No topic to clarify."}), 400
    text = find_followup(topic, kind, lang)
    return jsonify(spoken_payload(text, lang, topic))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
