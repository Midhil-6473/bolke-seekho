"""Open-ended DSA answers via any OpenAI-compatible chat API.

The curated approaches bank covers 41 algorithms. Any other search, and
any follow-up question about the algorithm on screen, goes to a
configured LLM in the same shape, so a student can ask ANY DSA question
instead of being limited to a fixed list. Standard library only
(urllib), so requirements.txt does not change.

Configure with environment variables (or the .env file):

  BOLKE_LLM_BASE_URL  e.g. http://localhost:11434/v1 (local Ollama),
                      or your provider's OpenAI-compatible base URL
  BOLKE_LLM_MODEL     e.g. qwen2.5:3b, gpt-oss:20b, ...
  BOLKE_LLM_API_KEY   optional; omit for local servers without auth

When unconfigured, unreachable, or failing, every function here returns
None and the caller falls back to the bank / family guides. The key is
never logged. Answers are AI-generated: the UI labels them "AI answer".
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

STRUCTURED_PROMPT = (
    "You are Bolke Seekho, a friendly DSA revision tutor for Indian college "
    "students. The student searched for a data structures or algorithms topic. "
    "If the search is not about data structures, algorithms, or coding-interview "
    "problem solving, reply with exactly this JSON and nothing else: "
    '{{"refused": true}}. Otherwise respond with JSON only — no markdown, no '
    "code fences, no extra text — with exactly this shape: "
    '{{"name": "Algorithm Name", "key_logic": "the core idea in 1-2 sentences, '
    'in {language}", "approaches": [{{"name": "Approach name", "logic": "how it '
    'works in 1-2 sentences, in {language}", "code": "the core Java method only, '
    '5-15 lines, assuming import java.util.*", "time": "O(...)", "space": "O(...)", '
    '"optimal": true/false}}]}}. List 2 to 4 genuinely different approaches, '
    "from simplest to best. Mark EXACTLY ONE approach optimal=true: the best "
    "technique to use in an interview. Write the name and approach names in "
    "English; write key_logic and logic in {language}. Keep code short and "
    "correct Java. Never invent problem numbers or company names."
)

FOLLOWUP_PROMPT = (
    "You are Bolke Seekho, a friendly DSA revision tutor for Indian college "
    "students. The student is looking at the algorithm below and asks a "
    "follow-up question about it. Answer ONLY about this algorithm and its "
    "approaches. If the question is not about data structures or algorithms, "
    "reply in one short sentence that you only answer DSA questions. Answer "
    "in {language}. Keep it short and spoken-friendly: 3 to 6 short sentences, "
    "simple words, plain text with no markdown formatting. Explain the idea, "
    "why it works, and the complexity or trade-off when relevant. "
    "If the student asks about a specific approach, answer about that approach. "
    "Never invent problem numbers or company names.\n\n"
    "Algorithm: {algorithm}\n"
    "Approaches on screen:\n{approaches}\n"
    "{focus}"
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


def _chat(messages, temperature=0.3, max_tokens=600) -> str | None:
    """One chat-completion call; the reply text, or None on any failure."""
    cfg = _config()
    if cfg is None:
        return None
    url, model, key = cfg
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
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


def llm_answer(question: str, lang: str) -> str | None:
    """Ask the configured LLM for a plain DSA answer, or None on failure."""
    language = LANG_NAMES.get(lang, "English")
    return _chat(
        [
            {"role": "system", "content": SYSTEM_PROMPT.format(language=language)},
            {"role": "user", "content": question},
        ],
        max_tokens=600,
    )


def llm_structured(question: str, lang: str) -> dict | None:
    """Ask the LLM for an algorithm in the approaches-bank shape.

    Returns a dict like an approaches.py entry (name, key_logic,
    approaches with name/logic/code/time/space/optimal), or None when
    unconfigured, failing, refused, or unparseable — the caller then
    falls back to a plain AI answer or the bank's guides.
    """
    language = LANG_NAMES.get(lang, "English")
    text = _chat(
        [
            {"role": "system", "content": STRUCTURED_PROMPT.format(language=language)},
            {"role": "user", "content": question},
        ],
        temperature=0.2,
        max_tokens=1600,
    )
    if not text:
        return None
    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.lower().startswith("json"):
            text = text[4:].strip()
    try:
        data = json.loads(text)
    except ValueError:
        return None
    if not isinstance(data, dict) or data.get("refused"):
        return None
    name = (data.get("name") or "").strip()
    key_logic = (data.get("key_logic") or "").strip()
    raw_approaches = data.get("approaches")
    if not name or not key_logic or not isinstance(raw_approaches, list):
        return None
    approaches = []
    for raw in raw_approaches[:5]:
        if not isinstance(raw, dict):
            continue
        approach = {
            "name": (raw.get("name") or "").strip(),
            "logic": (raw.get("logic") or "").strip(),
            "code": (raw.get("code") or "").strip(),
            "time": (raw.get("time") or "").strip(),
            "space": (raw.get("space") or "").strip(),
            "optimal": bool(raw.get("optimal")),
        }
        if approach["name"] and approach["logic"] and approach["code"]:
            approaches.append(approach)
    if len(approaches) < 2:
        return None
    # Exactly one optimal: keep the first marked, else mark the last
    # (models list approaches worst-to-best, so the last is the best bet).
    marked = [a for a in approaches if a["optimal"]]
    if len(marked) > 1:
        for extra in marked[1:]:
            extra["optimal"] = False
    elif not marked:
        approaches[-1]["optimal"] = True
    return {
        "name": name,
        "category": (data.get("category") or "Open DSA question").strip() or "Open DSA question",
        "key_logic": key_logic,
        "approaches": approaches,
    }


def llm_followup(question: str, lang: str, algorithm: str, approaches: list, focus: str = "") -> str | None:
    """Answer a follow-up question in the context of one algorithm.

    `approaches` is the list of approach dicts currently on screen, so
    the model answers about the methods the student can see. `focus` is
    the approach the student asked about, when they picked one.
    """
    language = LANG_NAMES.get(lang, "English")
    summary_lines = []
    for approach in approaches or []:
        line = "- {name}: {logic} (Time {time}, Space {space})".format(
            name=approach.get("name", ""),
            logic=approach.get("logic", ""),
            time=approach.get("time", "?"),
            space=approach.get("space", "?"),
        )
        summary_lines.append(line)
    focus_line = f"The student is asking about this approach: {focus}\n" if focus else ""
    system = FOLLOWUP_PROMPT.format(
        language=language,
        algorithm=algorithm,
        approaches="\n".join(summary_lines) or "(no approaches listed)",
        focus=focus_line,
    )
    return _chat(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
        max_tokens=600,
    )
