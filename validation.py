#!/usr/bin/env python3
"""
Validation utilities for translation payloads.
Ensures a strict schema before passing data to the UI.

Expected schema (dict):
{
  "original": str,
  "translation": str,
  "grammar": [
    {"word": str, "explanation": str, "function": str, ...}, ...
  ]
}

Returned normalized schema (dict):
{
  "original": str,
  "translation": str,
  "grammar": str,            # human-readable fallback text
  "grammar_json": list       # list of word objects
}
"""

from __future__ import annotations

from typing import Any, Dict, List, Union
import json


def _as_string(value: Any) -> str:
    return value if isinstance(value, str) else "" if value is None else str(value)


def _normalize_grammar_items(value: Any) -> List[Dict[str, Any]]:
    if isinstance(value, list):
        result: List[Dict[str, Any]] = []
        for item in value:
            if isinstance(item, dict):
                result.append({
                    "word": _as_string(item.get("word", "")).strip(),
                    "explanation": _as_string(item.get("explanation", "")).strip(),
                    "function": _as_string(item.get("function", "")).strip(),
                    "additional_info": _as_string(item.get("additional_info", "")).strip(),
                    "examples": _as_string(item.get("examples", "")).strip(),
                    "difficulty": _as_string(item.get("difficulty", "")).strip(),
                })
        # keep only entries that have at least word or explanation
        return [g for g in result if g["word"] or g["explanation"]]
    return []


def _build_grammar_text(items: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for item in items:
        word = item.get("word", "").strip()
        explanation = item.get("explanation", "").strip()
        function = item.get("function", "").strip()
        if not (word or explanation):
            continue
        line = f"- {word}: {explanation}" if word else f"- {explanation}"
        if function:
            line += f" ({function})"
        lines.append(line)
    return "\n".join(lines)


def parse_and_validate_translation(payload: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Parse a translation payload (JSON string or dict) and return a normalized dict.

    Never raises on malformed payloads; returns a minimal structure with empty fields instead.
    """
    original: str = ""
    translation: str = ""
    grammar_items: List[Dict[str, Any]] = []

    try:
        data: Dict[str, Any]
        if isinstance(payload, str):
            s = payload.strip()
            # Extract object if the string contains extra wrapper text
            start = s.find('{')
            end = s.rfind('}')
            if start != -1 and end != -1 and end > start:
                s = s[start:end+1]
            data = json.loads(s)
        elif isinstance(payload, dict):
            data = payload
        else:
            data = {}

        original = _as_string(data.get("original", "")).strip()
        translation = _as_string(data.get("translation", "")).strip()
        grammar_items = _normalize_grammar_items(data.get("grammar", []))
    except Exception:
        # keep defaults
        pass

    grammar_text = _build_grammar_text(grammar_items)

    return {
        "original": original,
        "translation": translation,
        "grammar": grammar_text,
        "grammar_json": grammar_items,
    }


