"""Bolke Seekho — a clean search-first DSA revision buddy (v3).

Search any algorithm: the app shows the key code first, then every
approach with its logic, Java code, time and space complexity, and the
best technique flagged. Ask follow-up questions about the algorithm or
one of its methods, and the voice agent answers in that context — by
text, or spoken aloud when a Gnani API key is set.

41 algorithms are curated in approaches.py (key code + approaches +
best pick). Anything else is answered by a configured LLM in the same
shape, so students are not limited to a fixed list. Voice uses Gnani
Prisma (speech-to-text) and Timbre (text-to-speech) in 10 languages.

Set GNANI_API_KEY (from app.gnani.ai) in the environment or in a .env
file. For open-ended answers, also set BOLKE_LLM_BASE_URL,
BOLKE_LLM_MODEL and optionally BOLKE_LLM_API_KEY (any OpenAI-compatible
chat API).
Run:  python app.py   then open http://127.0.0.1:5000
"""

import base64
import json
import os
import tempfile

from flask import Flask, jsonify, render_template, request

from answers import LANGUAGES, answer_query, find_followup
from approaches import ALGORITHMS, find_algorithm, suggest_algorithms
from llm import llm_answer, llm_followup, llm_structured

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


def _bank_entry(name: str) -> dict | None:
    """Approaches-bank entry by exact name (case-insensitive), or None."""
    wanted = (name or "").strip().lower()
    if not wanted:
        return None
    for entry in ALGORITHMS:
        if entry["name"].lower() == wanted:
            return entry
    return None


def _search(question: str, lang: str) -> dict:
    """Search one question: curated algorithm, LLM algorithm, or answer.

    Curated matches answer from the approaches bank (checked key code +
    approaches). Anything else goes to the LLM, first asking for the same
    structured shape, then for a plain answer. When no LLM is configured
    or it fails, the bank's family guide / not-in-list text is returned.
    """
    entry = find_algorithm(question)
    if entry is not None:
        result = {
            "kind": "algorithm",
            "source": "bank",
            "name": entry["name"],
            "category": entry["category"],
            "key_logic": entry["key_logic"],
            "approaches": entry["approaches"],
            "llm": False,
        }
        result["summary"] = _spoken_summary(result, lang)
        return result
    structured = llm_structured(question, lang)
    if structured is not None:
        structured.update({"kind": "algorithm", "source": "llm", "llm": True})
        structured["summary"] = _spoken_summary(structured, lang)
        return structured
    text = llm_answer(question, lang)
    if text:
        result = {
            "kind": "answer",
            "source": "llm",
            "topic": "AI answer",
            "answer": text,
            "category": "Open DSA question",
            "matched": False,
            "family": "",
            "suggestions": [],
            "llm": True,
        }
        result["summary"] = _spoken_summary(result, lang)
        return result
    result = answer_query(question, lang)
    out = {
        "kind": "answer",
        "source": "bank",
        "topic": result["topic"],
        "answer": result["answer"],
        "category": result["category"],
        "matched": result["matched"],
        "family": result["family"] or "",
        "suggestions": result["suggestions"],
        "llm": False,
    }
    out["summary"] = _spoken_summary(out, lang)
    return out


def _spoken_summary(result: dict, lang: str) -> str:
    """What the voice agent says after a voice search.

    Curated algorithms get the bank's spoken pattern-style answer in the
    user's language. LLM algorithms get their key logic plus the best
    approach. Plain answers are spoken as they are.
    """
    if result["kind"] == "answer":
        return result["answer"]
    if result["source"] == "bank":
        bank = answer_query(result["name"], lang)
        if bank["matched"] and bank["topic"] == result["name"]:
            return bank["answer"]
    best = next((a for a in result["approaches"] if a.get("optimal")), None)
    summary = result["key_logic"]
    if best is not None:
        summary += f" Best approach: {best['name']}, {best['time']} time, {best['space']} space."
    return summary


def _followup_answer(question: str, lang: str, algorithm: str, approach: str, client_approaches: list) -> tuple[str, bool, bool]:
    """Answer a question about the algorithm on screen.

    Returns (answer_text, llm_used, is_fallback). With an LLM configured,
    the model answers in the context of the algorithm and its approaches
    (optionally focused on one approach). Without one, the bank's spoken
    answer for the algorithm is the best available context answer.
    """
    entry = _bank_entry(algorithm)
    approaches = entry["approaches"] if entry is not None else (client_approaches or [])
    text = llm_followup(question, lang, algorithm, approaches, focus=approach)
    if text:
        return text, True, False
    bank = answer_query(algorithm, lang)
    return bank["answer"], False, True


@app.get("/")
def home():
    return render_template(
        "index.html",
        key_set=bool(API_KEY),
        languages=list(LANGUAGES.keys()),
    )


@app.get("/api/suggest")
def suggest():
    query = (request.args.get("q") or "").strip()
    try:
        limit = int(request.args.get("limit") or 6)
    except ValueError:
        limit = 6
    limit = max(1, min(limit, 10))
    return jsonify({"suggestions": suggest_algorithms(query, limit=limit)})


@app.post("/api/search")
def search():
    """Typed search. Works without an API key (text only)."""
    data = request.get_json(force=True, silent=True) or {}
    question = (data.get("question") or "").strip()
    lang = (data.get("lang") or "hinglish").lower()
    if not question:
        return jsonify({"error": "Type an algorithm to search for first.", "error_code": "EMPTY_QUESTION"}), 400
    result = _search(question, lang)
    result["voice_available"] = bool(API_KEY)
    result["answer_lang"] = _bank_lang(lang)
    return jsonify(result)


@app.post("/api/ask")
def ask_voice():
    """Voice search / voice follow-up. Needs a Gnani API key.

    Without an `algorithm` form field, the transcript is a fresh search
    and the spoken summary is returned with the result. With one, the
    transcript is a follow-up question about that algorithm (optionally
    focused on one `approach`), answered in context and spoken aloud.
    """
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
    algorithm = (request.form.get("algorithm") or "").strip()
    approach = (request.form.get("approach") or "").strip()
    client_approaches = []
    raw_approaches = (request.form.get("approaches") or "").strip()
    if raw_approaches:
        try:
            parsed = json.loads(raw_approaches)
            if isinstance(parsed, list):
                client_approaches = parsed
        except ValueError:
            client_approaches = []
    if algorithm:
        answer, llm_used, fallback = _followup_answer(transcript, lang, algorithm, approach, client_approaches)
        payload = spoken_payload(answer, lang, algorithm)
        payload.update(
            {
                "kind": "followup",
                "transcript": transcript,
                "algorithm": algorithm,
                "approach": approach,
                "llm": llm_used,
                "fallback": fallback,
                "answer_lang": _bank_lang(lang),
            }
        )
        return jsonify(payload)
    result = _search(transcript, lang)
    summary = _spoken_summary(result, lang)
    payload = spoken_payload(summary, lang, result.get("name") or result.get("topic", ""))
    payload.update(result)
    payload["transcript"] = transcript
    payload["spoken_summary"] = summary
    payload["answer_lang"] = _bank_lang(lang)
    return jsonify(payload)


@app.post("/api/followup")
def followup():
    """Follow-up question about the algorithm on screen.

    Body: {question, lang, algorithm, approach?, approaches?}. With an
    LLM configured the answer is context-aware; without one, the bank's
    answer for the algorithm is returned as a fallback. Spoken audio is
    included when a Gnani key is set. The legacy {topic, kind} form
    (simple/example clarifications) is still honoured.
    """
    data = request.get_json(force=True, silent=True) or {}
    lang = (data.get("lang") or "hinglish").lower()
    if "kind" in data and not (data.get("question") or "").strip():
        topic = (data.get("topic") or "").strip()
        kind = (data.get("kind") or "simple").strip()
        if not topic:
            return jsonify({"error": "No topic to clarify.", "error_code": "NO_TOPIC"}), 400
        if kind not in ("simple", "example"):
            kind = "simple"
        text = find_followup(topic, kind, lang)
        payload = spoken_payload(text, lang, topic)
        payload.update({"kind": kind, "answer_lang": _bank_lang(lang)})
        return jsonify(payload)
    question = (data.get("question") or "").strip()
    algorithm = (data.get("algorithm") or "").strip()
    approach = (data.get("approach") or "").strip()
    client_approaches = data.get("approaches") or []
    if not isinstance(client_approaches, list):
        client_approaches = []
    if not question:
        return jsonify({"error": "Type a question about the algorithm first.", "error_code": "EMPTY_QUESTION"}), 400
    if not algorithm:
        return jsonify({"error": "Search for an algorithm first, then ask about it.", "error_code": "NO_ALGORITHM"}), 400
    answer, llm_used, fallback = _followup_answer(question, lang, algorithm, approach, client_approaches)
    payload = spoken_payload(answer, lang, algorithm)
    payload.update(
        {
            "kind": "followup",
            "algorithm": algorithm,
            "approach": approach,
            "llm": llm_used,
            "fallback": fallback,
            "answer_lang": _bank_lang(lang),
        }
    )
    return jsonify(payload)


@app.post("/api/speak")
def speak_text():
    """Speak any text aloud (Listen buttons). Needs a Gnani API key."""
    if not API_KEY:
        return (
            jsonify({"error": "Voice needs a Gnani API key. Add GNANI_API_KEY to the .env file and restart.", "error_code": "NO_API_KEY"}),
            400,
        )
    data = request.get_json(force=True, silent=True) or {}
    text = (data.get("text") or "").strip()
    lang = (data.get("lang") or "hinglish").lower()
    if not text:
        return jsonify({"error": "Nothing to speak.", "error_code": "EMPTY_TEXT"}), 400
    payload = spoken_payload(text, lang)
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
