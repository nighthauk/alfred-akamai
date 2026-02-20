#!/usr/bin/env python3
"""
Action handler - copies the selected value to clipboard, or opens a URL in the browser.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import webbrowser

if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg.startswith("open::"):
        webbrowser.open(arg[6:])
    elif arg.startswith("update::"):
        path = arg[8:]
        if os.path.exists(path):
            # Copy to a temp path so we can safely delete the pending file
            # before Alfred opens it (avoids any race with the file being removed)
            tmp = tempfile.mktemp(suffix=".alfredworkflow")
            shutil.copy2(path, tmp)
            os.remove(path)
            subprocess.run(["open", tmp])
    else:
        print(arg)
