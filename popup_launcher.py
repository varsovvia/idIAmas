#!/usr/bin/env python3
"""
Popup launcher utility that encapsulates subprocess creation and environment handling.
Unified entrypoint to show the refactored popup.
"""

from __future__ import annotations

import os
import sys
import json
import tempfile
import subprocess
import uuid
from typing import Dict, Any, Optional


def launch_popup_subprocess(sections: Dict[str, Any]) -> Optional[subprocess.Popen]:
    """Launch the refactored popup in a subprocess and return the Popen handle or None.

    Silences stdout/stderr when TIMINGS_ONLY=1 and POPUP_DEBUG!=1.
    """
    # Allow simulation for tests or headless CI
    if os.getenv('POPUP_SIMULATE', '0') == '1':
        return None

    # Create a temporary file with the translation data
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(sections, f, ensure_ascii=False)
        temp_file = f.name

    popup_id = str(uuid.uuid4())[:8]
    script = f'''
import sys, json, os
sys.path.insert(0, r"{os.getcwd()}")
POPUP_ID = "{popup_id}"
try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    from popup_refactored import PopupWindow

    with open(r"{temp_file}", 'r', encoding='utf-8') as f:
        data = json.load(f)

    app = QApplication(sys.argv)
    popup = PopupWindow(data)
    popup.setWindowTitle(f"idIAmas [{{POPUP_ID}}]")
    popup.setWindowFlags(popup.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
    popup.show(); popup.raise_(); popup.activateWindow()
    app.exec()
except Exception as e:
    import traceback; traceback.print_exc()
finally:
    try:
        os.unlink(r"{temp_file}")
    except Exception:
        pass
'''

    # Write the script to a temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(script)
        script_file = f.name

    # Configure suppression based on env flags
    suppress = os.getenv('TIMINGS_ONLY', '0') == '1' and os.getenv('POPUP_DEBUG', '0') != '1'
    stdout = subprocess.DEVNULL if suppress else None
    stderr = subprocess.DEVNULL if suppress else None

    if sys.platform == 'win32':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        process = subprocess.Popen([sys.executable, script_file], startupinfo=startupinfo, stdout=stdout, stderr=stderr)
    else:
        process = subprocess.Popen([sys.executable, script_file], stdout=stdout, stderr=stderr)

    return process


