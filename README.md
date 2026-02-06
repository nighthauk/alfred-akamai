# Akamai Account Search Alfred Workflow

A productivity workflow for [Alfred](https://www.alfredapp.com/) that enables quick searching of Akamai account switch keys using the Identity & Access Management (IAM) API.

## Overview

This workflow allows you to search for and quickly copy Akamai account switch keys directly from Alfred's search bar. It's designed for developers, DevOps engineers, and anyone working with multiple Akamai accounts who needs to frequently access account switch keys for API operations or CLI tools.

## Features

- **Fast Search**: Query Akamai accounts by name with real-time results
- **One-Click Copy**: Press Enter to copy the account switch key to clipboard
- **Alternative Copy**: Hold Option+Enter to copy the account name instead
- **Secure Authentication**: Uses Akamai's official EdgeGrid authentication
- **Configurable**: Customizable edgerc path and section

## Requirements

- **Alfred 5** with [Powerpack](https://www.alfredapp.com/powerpack/)
- **Python 3.9+**
- **Akamai API Credentials** (with access to IAM API)
- **edgegrid-python** library

## Installation

### Option 1: Pre-built Workflow

1. Download the latest `Akamai-Account-Search.alfredworkflow` from the [releases page](https://github.com/yourusername/alfred-akamai/releases)
2. Double-click the downloaded file to install
3. Configure your credentials (see Setup below)

### Option 2: Build from Source

```bash
git clone https://github.com/yourusername/alfred-akamai.git
cd alfred-akamai
./build.sh
# Double-click Akamai-Account-Search.alfredworkflow
```

## Setup

### 1. Install Python Dependencies

```bash
pip3 install edgegrid-python requests
```

### 2. Configure Akamai Credentials

Create or edit your `~/.edgerc` file with your Akamai API credentials:

```ini
[default]
client_secret = your_client_secret
host = your_host.akamaiapis.net
access_token = your_access_token
client_token = your_client_token
```

### 3. Configure the Workflow

1. Open Alfred and search for "Akamai Account Search"
2. Click the **[x]** icon to open workflow settings
3. Enter your **Client ID** (required) - found in Akamai Identity & Access Management
4. Optionally adjust the **edgerc Path** (default: `~/.edgerc`)
5. Optionally adjust the **edgerc Section** (default: `default`)

## Usage

1. Open Alfred (Cmd+Space)
2. Type `akamai` followed by your search query
3. Select an account from the results
4. Press **Enter** to copy the account switch key to clipboard

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Enter** | Copy account switch key |
| **Option+Enter** | Copy account name |
| **Escape** | Dismiss results |

### Example

```
# Search for accounts containing "production"
akamai production

# Search for a specific customer
akamai acme corp
```

## Project Structure

```
alfred-akamai/
├── Akamai Account Search.alfredworkflow/
│   ├── search.py          # Main script filter for searching
│   ├── action.py          # Action handler for clipboard operations
│   ├── edgegrid.py        # EdgeGrid authentication wrapper
│   ├── icon.png           # Workflow icon
│   └── info.plist         # Workflow configuration
├── build.sh               # Build script for .alfredworkflow
└── README.md              # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| [`search.py`](Akamai%20Account%20Search.alfredworkflow/search.py) | Main Alfred script filter that handles search queries and API communication |
| [`action.py`](Akamai%20Account%20Search.alfredworkflow/action.py) | Handles the selected result and copies it to clipboard |
| [`edgegrid.py`](Akamai%20Account%20Search.alfredworkflow/edgegrid.py) | Wrapper around the official Akamai EdgeGrid authentication library |
| [`info.plist`](Akamai%20Account%20Search.alfredworkflow/info.plist) | Alfred workflow configuration and UI definitions |
| [`build.sh`](build.sh) | Script to package the workflow into a distributable `.alfredworkflow` file |

## API Reference

This workflow uses the [Akamai IAM API](https://techdocs.akamai.com/iam-api/reference/get-client-account-switch-keys):

- **Endpoint**: `/identity-management/v3/api-clients/{clientId}/account-switch-keys`
- **Method**: GET
- **Parameters**: `search` (account name filter)

## Troubleshooting

### "Client ID Required" Error
- Open workflow settings and ensure your Client ID is correctly entered

### "Edgerc Not Found" Error
- Verify your `~/.edgerc` file exists and contains valid credentials
- Check the edgerc Path setting in workflow configuration

### "API Error" Response
- Ensure your API credentials have access to the IAM API
- Verify your account switch keys exist and are accessible

### No Results Found
- Search requires at least 3 characters
- Check that your account names contain the search query

## Development

### Running Locally

```bash
# Test search functionality
cd "Akamai Account Search.alfredworkflow"
python3 search.py "test"
```

### Building the Workflow

```bash
./build.sh
```

This creates `Akamai-Account-Search.alfredworkflow` in the project root.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [Akamai Technologies](https://www.akamai.com/) for the EdgeGrid authentication library
- [Alfred](https://www.alfredapp.com/) for this excellent productivity tool

---

**Note**: This workflow is not officially maintained by Akamai. For support, please open an issue on GitHub.
