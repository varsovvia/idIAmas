import os
from popup_launcher import launch_popup_subprocess


def test_launch_popup_simulated(monkeypatch):
    monkeypatch.setenv('POPUP_SIMULATE', '1')
    sections = {
        'original': 'Ciao',
        'translation': 'Hola',
        'grammar': '- Ciao: Hola (interjección)',
        'grammar_json': [
            {'word': 'Ciao', 'explanation': 'Hola', 'function': 'interjección'}
        ],
    }
    proc = launch_popup_subprocess(sections)
    assert proc is None

