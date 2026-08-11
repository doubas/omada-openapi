# Omada OpenAPI Skill

This Codex skill safely controls the TP-Link Omada controller through its OpenAPI.

## Included

- A Bash OpenAPI wrapper with controller-token authentication
- Workspace fixes for WSL DNS and Windows CRLF `.env` files
- Verified site, client, and device discovery patterns

## Setup

Place these variables in the workspace `.env` file. Do not commit that file.

```text
OMADA_URL=https://omada-ip:8043/
OMADA_CLIENT=your-client-id
OMADA_SECRET=your-client-secret
```

The local Linux environment needs `curl` and `jq`.

## Example

```bash
bash -lc 'bash .agents/skills/omada-openapi/scripts/omada-api.sh GET "/sites?pageSize=100&page=1"'
```

Retrieve the `siteId` before issuing site-scoped requests. Confirm exact targets before making configuration-changing API calls.
