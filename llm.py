"""Open-ended DSA answers via any OpenAI-compatible chat API.

The curated answer bank answers the 40 listed topics. Any other question
goes to a configured LLM, so a student can ask ANY DSA question instead
of being limited to a fixed list. Standard library only (urllib), so
requirements.txt does not change.

Configure with environment variables (or the .env file):

  BOLKE_LLM_BASE_URL  e.g. http://localhost:11434/v1 (local Ollama),
                      or your provider's OpenAI-compatible base URL
  BOLKE_LLM_MODEL     e.g. qwen2.5:3b, gpt-oss:20b, ...
  BOLKE_LLM_API_KEY   optional; omit for local servers without auth

When unconfigured, unreachable, or failing, llm_answer() returns None
and the caller falls back to the bank / family guides. The key is never
logged. Answers are AI-generated: the UI labels them "AI answer".
"""

import json
import os
import urllib.error
import urllib.request

LANG_NAMES = {
    "hinglish": "Hinglish (Hindi mixed with English, written in Roman script)",
    "english": "English",
    "telugu": "Telugu",
    "tamil": "Tamil",
    "kannada": "Kannada",
    "malayalam": "Malayalam",
    "marathi": "Marathi",
    "bengali": "Bengali",
    "gujarati": "Gujarati",
    "punjabi": "Punjabi",
}

SYSTEM_PROMPT = (
    "You are Bolke Seekho, a friendly DSA revision tutor for Indian college "
    "students. Answer ONLY data structures and algorithms questions. If the "
    "question is not about data structures, algorithms, or coding-interview "
    "problem solving, reply in one short sentence that you only answer DSA "
    "questions. Answer in {language}. Explain the PATTERN first: name it, say "
    "why it works in simple words, give the time and space complexity, and "
    "end with the trade-off or interview tip. Keep it short and spoken-friendly: "
    "4 to 7 short sentences, simple words, plain text with no markdown "
    "formatting and no long code. A tiny 3 to 5 line sketch is allowed only "
    "if it makes the idea clearer. Never invent problem numbers or company names."
)


def _config():
    """Return (url, model, api_key) or None when not configured."""
    base = os.environ.get("BOLKE_LLM_BASE_URL", "").strip().rstrip("/")
    model = os.environ.get("BOLKE_LLM_MODEL", "").strip()
    key = os.environ.get("BOLKE_LLM_API_KEY", "").strip()
    if not base or not model:
        return None
    if not base.endswith("/chat/completions"):
        base += "/chat/completions"
    return base, model, key


def llm_configured() -> bool:
    return _config() is not None


def llm_answer(question: str, lang: str) -> str | None:
    """Ask the configured LLM for a DSA answer, or None on any failure."""
    cfg = _config()
    if cfg is None:
        return None
    url, model, key = cfg
    language = LANG_NAMES.get(lang, "English")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT.format(language=language)},
            {"role": "user", "content": question},
        ],
        "temperature": 0.3,
        "max_tokens": 600,
    }
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = "Bearer " + key
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read(65536)
    except (urllib.error.URLError, OSError, TimeoutError):
        return None
    try:
        data = json.loads(raw.decode("utf-8"))
        text = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        return None
    text = (text or "").strip()
    return text or None
