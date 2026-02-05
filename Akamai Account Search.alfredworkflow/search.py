#!/usr/bin/env python3
"""
Alfred Script Filter for Akamai Account Search.
Configuration is done via Alfred's workflow configuration panel.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from edgegrid import EdgeGridAuth


def get_config():
    """Get configuration from Alfred environment variables."""
    return {
        'client_id': os.environ.get('client_id', ''),
        'edgerc_path': os.path.expanduser(os.environ.get('edgerc_path', '~/.edgerc')),
        'edgerc_section': os.environ.get('edgerc_section', 'default')
    }


def alfred_item(title, subtitle, arg="", valid=True):
    """Create an Alfred result item."""
    return {"title": title, "subtitle": subtitle, "arg": arg, "valid": valid}


def alfred_output(items):
    """Create Alfred JSON output."""
    return json.dumps({"items": items})


def search_accounts(query, config):
    """Search for account switch keys via API."""
    try:
        auth = EdgeGridAuth.from_edgerc(config['edgerc_path'], config['edgerc_section'])
        path = f"/identity-management/v3/api-clients/{config['client_id']}/account-switch-keys"
        params = {'search': query}
        response = auth.make_request('GET', path, params=params)

        if response.get('status') == 200:
            accounts = response.get('data', [])
            if not accounts:
                return alfred_output([alfred_item(
                    "No accounts found",
                    f"No accounts matching '{query}'",
                    valid=False
                )])

            items = []
            for acc in accounts:
                name = acc.get('accountName', 'Unknown')
                key = acc.get('accountSwitchKey', '')
                items.append({
                    "title": name,
                    "subtitle": key,
                    "arg": key,
                    "valid": True,
                    "mods": {
                        "alt": {"subtitle": "Copy account name", "arg": name}
                    },
                    "text": {"copy": key, "largetype": f"{name}\n{key}"}
                })
            return alfred_output(items)

        error = response.get('error', {})
        if isinstance(error, dict):
            msg = error.get('detail') or error.get('title') or error.get('message') or str(error)
        else:
            msg = str(error)
        return alfred_output([alfred_item("API Error", f"Status {response.get('status')}: {msg}", valid=False)])

    except FileNotFoundError as e:
        return alfred_output([alfred_item("EdgeRC Not Found", str(e), valid=False)])
    except Exception as e:
        return alfred_output([alfred_item("Error", str(e), valid=False)])


def main():
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else ""
    config = get_config()

    # No query - prompt to search
    if not query:
        print(alfred_output([alfred_item(
            "Search for accounts...",
            "Type an account name to search",
            valid=False
        )]))
        return

    # Check configuration
    if not config['client_id']:
        print(alfred_output([alfred_item(
            "Configuration Required",
            "Open workflow settings to set Client ID (click [x] icon)",
            valid=False
        )]))
        return

    if not os.path.exists(config['edgerc_path']):
        print(alfred_output([alfred_item(
            "EdgeRC Not Found",
            f"File not found: {config['edgerc_path']}",
            valid=False
        )]))
        return

    # Check minimum query length
    if len(query) < 3:
        print(alfred_output([alfred_item(
            "Keep typing...",
            "Enter at least 3 characters to search",
            valid=False
        )]))
        return

    # Search
    print(search_accounts(query, config))


if __name__ == '__main__':
    main()
