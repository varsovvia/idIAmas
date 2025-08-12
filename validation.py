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
import re


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
            # Remove common code fences if present
            if s.startswith('```'):
                s = s.strip('`')
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
        # Fallback: regex-based extraction from raw text even if JSON is malformed/codefenced
        try:
            s = payload if isinstance(payload, str) else json.dumps(payload)
            # Strip code fences
            s = re.sub(r"```(json)?", "", s)
            # Pull original/translation if present
            m_orig = re.search(r'"original"\s*:\s*"([\s\S]*?)"', s)
            m_trans = re.search(r'"translation"\s*:\s*"([\s\S]*?)"', s)
            if m_orig:
                original = m_orig.group(1).strip()
            if m_trans:
                translation = m_trans.group(1).strip()
            # Try grammar array extraction
            m_gram = re.search(r'"grammar"\s*:\s*(\[[\s\S]*?\])', s)
            if m_gram:
                gram_str = m_gram.group(1)
                try:
                    grammar_items = json.loads(gram_str)
                except Exception:
                    # Attempt to repair trailing comma issues
                    gram_repaired = re.sub(r",\s*\]", "]", gram_str)
                    try:
                        grammar_items = json.loads(gram_repaired)
                    except Exception:
                        # Last resort: extract per-item objects with regex
                        obj_matches = re.findall(r"\{[\s\S]*?\}", gram_str)
                        extracted: List[Dict[str, Any]] = []
                        for obj in obj_matches:
                            def _field(name: str) -> str:
                                m = re.search(fr'"{name}"\s*:\s*"([\s\S]*?)"', obj)
                                return m.group(1).strip() if m else ""
                            item = {
                                'word': _field('word'),
                                'explanation': _field('explanation'),
                                'function': _field('function'),
                                'additional_info': _field('additional_info'),
                                'examples': _field('examples'),
                                'difficulty': _field('difficulty'),
                            }
                            if item['word'] or item['explanation']:
                                extracted.append(item)
                        grammar_items = extracted
        except Exception:
            # keep defaults if everything fails
            pass

    grammar_text = _build_grammar_text(grammar_items)

    return {
        "original": original,
        "translation": translation,
        "grammar": grammar_text,
        "grammar_json": grammar_items,
    }


