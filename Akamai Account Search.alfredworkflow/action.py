#!/usr/bin/env python3
"""
Action handler - copies the selected value to clipboard, or opens a URL in the browser.
"""

import sys
import webbrowser

if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg.startswith("open::"):
        webbrowser.open(arg[6:])
    else:
        print(arg)
