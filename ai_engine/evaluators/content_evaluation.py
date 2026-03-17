"""
Content Evaluation Module
Uses Groq LLM to score transcript quality and generate a teaching summary.

Input:  transcript text (str)
Output: structured dict with numeric scores, strengths, weaknesses, and summary
"""

from typing import Dict, List
from ai_engine.models.groq_client import GroqClient

# ── Prompts ────────────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = (
    "You are an expert educational content evaluator. "
    "Respond ONLY with valid JSON — no markdown, no extra text."
)

_EVAL_PROMPT = """Analyze the following transcript from a teaching/mentoring session.
The text may contain Hindi, English, or Hinglish (mixed).

Evaluate on these four dimensions:
1. Clarity (0-100): How clear and understandable is the explanation?
2. Structure (0-100): Is content well-organized with logical flow?
3. Technical Accuracy (0-100): Are concepts explained correctly?
4. Engagement (0-100): Does the teacher use engaging language, examples, or questions?

Transcript:
{transcript}

Respond ONLY with this JSON (no other text):
{{
  "clarity": <number 0-100>,
  "structure": <number 0-100>,
  "technical": <number 0-100>,
  "engagement": <number 0-100>,
  "summary": "<1-2 sentence summary in English>"
}}"""

_SUMMARY_PROMPT = """Analyze the full transcript of a teaching session below.
The text may contain Hindi, English, or Hinglish.

Full Transcript:
{transcript}

Provide a comprehensive evaluation in this JSON format (no other text):
{{
  "topic": "<what the teacher was explaining — 1 sentence>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "weaknesses": ["<area 1>", "<area 2>"],
  "summary": "<overall 2-3 sentence teaching summary in English>"
}}"""


# ── Public API ─────────────────────────────────────────────────────────────────

def evaluate_content(transcript: str, groq_client: GroqClient = None) -> Dict:
    """
    Score a single transcript chunk with the Groq LLM.

    Args:
        transcript:  Text to evaluate (can be a chunk or full transcript).
        groq_client: Optional pre-constructed GroqClient (for dependency injection).

    Returns:
        Dict with keys: ``clarity``, ``structure``, ``technical``,
        ``engagement``, ``summary``, ``success`` (bool), and optionally ``error``.
    """
    if not transcript or len(transcript.strip()) < 10:
        return _neutral_scores(error="Transcript too short for meaningful evaluation")

    client = groq_client or GroqClient()
    try:
        data = client.chat_json(
            system_prompt=_SYSTEM_PROMPT,
            user_prompt=_EVAL_PROMPT.format(transcript=transcript),
            temperature=0.3,
            max_tokens=500,
        )
        return _validate_eval(data)
    except Exception as exc:
        return _neutral_scores(error=str(exc))


def generate_summary(full_transcript: str, groq_client: GroqClient = None) -> Dict:
    """
    Generate a holistic teaching summary from the complete transcript.

    Args:
        full_transcript: Concatenated transcript of the full session.
        groq_client:     Optional pre-constructed GroqClient.

    Returns:
        Dict with keys: ``topic`` (str), ``strengths`` (list[str]),
        ``weaknesses`` (list[str]), ``summary`` (str),
        ``success`` (bool), and optionally ``error``.
    """
    if not full_transcript or len(full_transcript.strip()) < 10:
        return _empty_summary(error="Transcript too short")

    client = groq_client or GroqClient()
    try:
        data = client.chat_json(
            system_prompt=_SYSTEM_PROMPT,
            user_prompt=_SUMMARY_PROMPT.format(transcript=full_transcript),
            temperature=0.3,
            max_tokens=800,
        )
        return _validate_summary(data)
    except Exception as exc:
        return _empty_summary(error=str(exc))


def aggregate_chunk_evals(evals: List[Dict]) -> Dict:
    """
    Average scores across multiple chunk evaluations.

    Args:
        evals: List of dicts from ``evaluate_content()``.

    Returns:
        Aggregated dict with averaged numeric scores and ``success`` flag.
    """
    valid = [e for e in evals if e.get("success")]
    if not valid:
        return _neutral_scores(error="No successful chunk evaluations")

    keys = ("clarity", "structure", "technical", "engagement")
    result = {k: round(sum(e[k] for e in valid) / len(valid), 1) for k in keys}
    result["success"] = True
    return result


# ── Private helpers ────────────────────────────────────────────────────────────

def _validate_eval(data: Dict) -> Dict:
    required = {"clarity", "structure", "technical", "engagement", "summary"}
    if not required.issubset(data.keys()):
        return _neutral_scores(error="LLM response missing required fields")

    for key in ("clarity", "structure", "technical", "engagement"):
        try:
            data[key] = max(0.0, min(100.0, float(data[key])))
        except (ValueError, TypeError):
            return _neutral_scores(error=f"Invalid score for '{key}'")

    data["summary"] = str(data.get("summary", ""))
    data["success"] = True
    return data


def _validate_summary(data: Dict) -> Dict:
    data.setdefault("topic", "Unknown topic")
    data["strengths"] = _ensure_list(data.get("strengths", []))
    data["weaknesses"] = _ensure_list(data.get("weaknesses", []))
    data["summary"] = str(data.get("summary", ""))
    data["success"] = True
    return data


def _ensure_list(value) -> List[str]:
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str):
        return [value] if value else []
    return []


def _neutral_scores(error: str = "") -> Dict:
    return {
        "clarity": 50.0,
        "structure": 50.0,
        "technical": 50.0,
        "engagement": 50.0,
        "summary": "Content evaluation unavailable",
        "success": False,
        "error": error,
    }


def _empty_summary(error: str = "") -> Dict:
    return {
        "topic": "Unknown",
        "strengths": [],
        "weaknesses": [],
        "summary": "Summary unavailable",
        "success": False,
        "error": error,
    }
