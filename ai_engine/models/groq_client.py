"""
Groq Client Module
Wraps Groq API for LLM-based content evaluation calls.
Encapsulates all Groq API interaction so evaluators stay thin.
"""

import os
import json
from dotenv import load_dotenv
from typing import Any, Dict, Optional
from groq import Groq


# Lazy-loaded singleton
_client: Optional[Groq] = None


def _get_client() -> Groq:
    """
    Return the cached Groq client, initializing it on first call.

    Raises:
        ValueError: If GROQ_API_KEY is not set in environment.
    """
    global _client
    if _client is None:
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is not set. "
                "Get a free key at https://console.groq.com/keys and add it to .env."
            )
        _client = Groq(api_key=api_key)
    return _client


class GroqClient:
    """
    Thin wrapper around the Groq chat-completion API.

    Usage:
        client = GroqClient()
        result = client.chat_json(system_prompt, user_prompt)
    """

    def __init__(self, model: str = "llama-3.1-8b-instant"):
        """
        Args:
            model: Groq model identifier (default: llama-3.1-8b-instant).
        """
        self.model = model

    def chat_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 800,
    ) -> Dict[str, Any]:
        """
        Send a chat completion request and parse the response as JSON.

        The method handles common LLM JSON formatting issues — it will try a
        direct JSON parse first, then fall back to extracting the first
        ``{...}`` block from the response text.

        Args:
            system_prompt: Instruction/role for the LLM.
            user_prompt:   The actual content to process.
            temperature:   Sampling temperature (lower = more deterministic).
            max_tokens:    Maximum tokens in the response.

        Returns:
            Parsed JSON dictionary from the LLM response.

        Raises:
            ValueError: If the response cannot be parsed as valid JSON.
            Exception:  Propagates any Groq API errors.
        """
        client = _get_client()

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        raw = response.choices[0].message.content or ""
        return self._parse_json(raw)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_json(text: str) -> Dict[str, Any]:
        """
        Parse JSON from an LLM text response.

        Tries direct parse first; falls back to extracting the first { … } block.

        Raises:
            ValueError: If no valid JSON object is found.
        """
        # Attempt 1: direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Attempt 2: extract first {...} block
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass

        raise ValueError(f"Could not parse JSON from LLM response:\n{text[:500]}")
