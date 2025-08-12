import json
from validation import parse_and_validate_translation


def test_parse_dict_valid_schema():
    payload = {
        "original": "Ciao",
        "translation": "Hola",
        "grammar": [
            {"word": "Ciao", "explanation": "Hola", "function": "interjección"}
        ],
    }
    result = parse_and_validate_translation(payload)
    assert result["original"] == "Ciao"
    assert result["translation"] == "Hola"
    assert isinstance(result["grammar_json"], list)
    assert "- Ciao: Hola (interjección)" in result["grammar"]


def test_parse_string_with_extra_text():
    s = "Result: {\n  \"original\": \"Ciao\", \n  \"translation\": \"Hola\", \n  \"grammar\": []\n } End"
    result = parse_and_validate_translation(s)
    assert result["original"] == "Ciao"
    assert result["translation"] == "Hola"
    assert result["grammar_json"] == []


def test_parse_malformed_returns_defaults():
    result = parse_and_validate_translation("not-json")
    assert result["original"] == ""
    assert result["translation"] == ""
    assert result["grammar_json"] == []

