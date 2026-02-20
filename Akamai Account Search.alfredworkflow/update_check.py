#!/usr/bin/env python3
"""
Background update checker for Akamai Account Search.
Spawned by search.py; exits silently on any error.
"""

import json
import os
import sys
import time
import urllib.request

RELEASES_URL = "https://api.github.com/repos/nighthauk/alfred-akamai/releases/latest"
CHECK_INTERVAL = 28800  # seconds between checks (4 hours)


def main():
    cache_dir = sys.argv[1] if len(sys.argv) > 1 else ""
    if not cache_dir:
        return

    state_file = os.path.join(cache_dir, "state.txt")
    update_file = os.path.join(cache_dir, "pending_update.alfredworkflow")

    # Throttle: skip if we checked recently (use state file mtime as last-check marker)
    if os.path.exists(state_file):
        if time.time() - os.path.getmtime(state_file) < CHECK_INTERVAL:
            return

    try:
        current_state = ""
        if os.path.exists(state_file):
            with open(state_file) as f:
                current_state = f.read().strip()

        with urllib.request.urlopen(RELEASES_URL, timeout=10) as resp:
            release = json.loads(resp.read())

        release_id = str(release.get("id", ""))

        os.makedirs(cache_dir, exist_ok=True)

        if release_id == current_state:
            # Touch state file to reset the check timer
            os.utime(state_file, None)
            return

        # Find the .alfredworkflow asset
        download_url = None
        for asset in release.get("assets", []):
            if asset["name"].endswith(".alfredworkflow"):
                download_url = asset["browser_download_url"]
                break

        if not download_url:
            return

        with urllib.request.urlopen(download_url, timeout=30) as resp:
            with open(update_file, "wb") as f:
                f.write(resp.read())

        with open(state_file, "w") as f:
            f.write(release_id)

    except Exception:
        pass


if __name__ == "__main__":
    main()
