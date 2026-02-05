#!/usr/bin/env python3
"""
EdgeGrid authentication using the official edgegrid-python library.
Install: pip3 install edgegrid-python requests
"""

import os
import sys

# Add common user site-packages locations
for pyver in ['3.13', '3.12', '3.11', '3.10', '3.9']:
    site = os.path.expanduser(f"~/Library/Python/{pyver}/lib/python/site-packages")
    if os.path.exists(site) and site not in sys.path:
        sys.path.insert(0, site)

import requests
from akamai.edgegrid import EdgeGridAuth as AkamaiEdgeGridAuth, EdgeRc


class EdgeGridAuth:
    """Wrapper around official Akamai EdgeGrid authentication."""

    def __init__(self, edgerc_path, section='default'):
        self.edgerc_path = os.path.expanduser(edgerc_path)
        self.section = section
        self._session = None
        self._base_url = None
        self._setup()

    def _setup(self):
        """Initialize EdgeGrid auth from edgerc file."""
        if not os.path.exists(self.edgerc_path):
            raise FileNotFoundError(f"EdgeRC file not found: {self.edgerc_path}")

        edgerc = EdgeRc(self.edgerc_path)
        self._base_url = f"https://{edgerc.get(self.section, 'host')}"
        self._session = requests.Session()
        self._session.auth = AkamaiEdgeGridAuth.from_edgerc(edgerc, self.section)

    @classmethod
    def from_edgerc(cls, edgerc_path, section='default'):
        """Create instance from edgerc file."""
        return cls(edgerc_path, section)

    def make_request(self, method, path, params=None, body=None, headers=None):
        """Make authenticated API request."""
        url = f"{self._base_url}{path}"

        req_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        if headers:
            req_headers.update(headers)

        try:
            response = self._session.request(
                method=method.upper(),
                url=url,
                params=params,
                json=body,
                headers=req_headers,
                timeout=30
            )

            result = {'status': response.status_code}
            try:
                result['data'] = response.json()
            except:
                result['data'] = response.text

            if response.status_code >= 400:
                result['error'] = result.get('data', {})

            return result

        except requests.exceptions.RequestException as e:
            return {'status': 0, 'error': {'message': str(e)}}
