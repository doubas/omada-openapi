# Omada SDN Controller Open API Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Omada: v5.9+](https://img.shields.io/badge/Omada%20SDN-v5.9+-orange.svg)](https://www.tp-link.com/business-networking/omada-sdn/)

A modular, production-ready AI agent skill and developer CLI for interacting with **TP-Link Omada SDN Controllers** via the official Open API (OpenAPI 3.0.1).

Designed for seamless integration with AI coding assistants (Antigravity, Gemini, Claude, OpenAI) and standalone command-line network operations.

---

## 🚀 Features

- **Cross-Platform Python CLI (`scripts/omada_cli.py`)**: Runs natively on Windows (PowerShell/CMD), macOS, and Linux without requiring `curl` or `jq`.
- **Bash Automation Wrapper (`scripts/omada-api.sh`)**: Unix/WSL shell script with built-in token lifecycle management and formatting.
- **Automated Authentication**: Seamless OAuth2 token acquisition (`POST /openapi/authorize/token?grant_type=client_credentials`) with automatic token reuse and header injection (`Authorization: AccessToken=<token>`).
- **Comprehensive Controller Queries**: Built-in commands for sites, hardware devices (APs, switches, gateways), active clients, LAN networks, and arbitrary REST endpoints.
- **Safety First**: Non-destructive defaults, automatic dry-run validation, and explicit confirmation prompts for configuration-modifying endpoints.

---

## 📋 Compatibility

- **Omada SDN Controller**: v5.9 or later (Software Controller, Cloud-Based Controller, OC200, OC300).
- **Authentication**: Requires the **Open API** feature enabled under **Global View > Settings > Platform Integration > Open API** with application type set to **Client**.
- **Dependencies**: Python 3.8+ with `requests` (`pip install requests urllib3`).

---

## ⚙️ Environment Setup

Copy `.env.example` to `.env` in your workspace root and configure your controller URL and credentials:

```ini
# Base URL of the Omada Controller (typically port 8043)
OMADA_URL=https://omada.example.com:8043

# Open API Client Credentials
OMADA_CLIENT_ID=your-client-id
OMADA_CLIENT_SECRET=your-client-secret

# Controller ID and Target Site ID (Optional: auto-discovered if omitted)
OMADA_ID=your-omada-controller-id
OMADA_SITE_ID=your-target-site-id

# Set to 1 to trust local self-signed TLS certificates
OMADA_INSECURE_TLS=1
```

> [!CAUTION]
> Never commit your `.env` file containing secrets to version control. Ensure it is included in `.gitignore`.

---

## 🛠️ CLI Usage Guide

### 1. Python CLI (`scripts/omada_cli.py`)

#### Test Connectivity & Authentication
Verifies API credentials, acquires an access token, discovers the controller ID, and lists available sites:
```bash
python scripts/omada_cli.py test
```

#### List Sites
```bash
python scripts/omada_cli.py sites
# Output in JSON:
python scripts/omada_cli.py sites --json
```

#### List Managed Hardware (APs, Switches, Gateways)
Displays IP addresses, MAC addresses, models, and real-time status:
```bash
python scripts/omada_cli.py devices
```

#### List Connected Network Clients
Displays active wired and wireless clients with assigned IP, MAC, VLAN, and SSID/Port:
```bash
python scripts/omada_cli.py clients
```

#### Execute Arbitrary Open API Requests
Send arbitrary GET, POST, PUT, PATCH, or DELETE requests relative to `/openapi/v1/{omadacId}`:
```bash
# Query site-specific devices
python scripts/omada_cli.py request GET sites/{siteId}/devices

# Reboot a device
python scripts/omada_cli.py request POST sites/{siteId}/cmd/devices/reboot '{"deviceMacs":["AA-BB-CC-DD-EE-FF"]}'
```

---

### 2. Bash API Wrapper (`scripts/omada-api.sh`)

For Linux, macOS, and WSL environments:

```bash
# Health check & verify credentials
bash scripts/omada-api.sh

# List sites
bash scripts/omada-api.sh GET "/sites?page=1&pageSize=100"

# List devices at a site
bash scripts/omada-api.sh GET "/sites/{siteId}/devices?page=1&pageSize=100"
```

---

## 📚 References & Architecture

- [references/api-categories.md](references/api-categories.md): Breakdown of the 1,507+ endpoints across 100+ categories defined in the Omada OpenAPI spec.
- [references/external-resources.md](references/external-resources.md): Links to official TP-Link Open API documentation and Swagger specifications.
- [references/example-topology.md](references/example-topology.md): Example network topology, VLAN architecture, and switch allocation.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
