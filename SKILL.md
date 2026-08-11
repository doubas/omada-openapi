---
name: omada-openapi
description: Control TP-Link Omada controllers through their OpenAPI. Use when inspecting or changing Omada sites, clients, access points, switches, gateways, VLANs, WLANs, firewall rules, VPNs, or controller configuration.
---

# Omada OpenAPI

Use `scripts/omada-api.sh` for every controller API request. It loads `.env` from the workspace, obtains a controller token, and formats responses with `jq`.

## Safety

- Start with a read-only health check and then retrieve the required IDs.
- Treat GET requests as read-only. Before POST, PUT, PATCH, DELETE, reboot, firmware, or configuration changes, describe the exact target and request confirmation.
- Do not print or commit `.env`, access tokens, client secrets, or backups.
- Check `errorCode`; `0` means success.

## Commands

Run all calls through Bash so query strings retain `&`:

```bash
bash -lc 'bash .agents/skills/omada-openapi/scripts/omada-api.sh'
bash -lc 'bash .agents/skills/omada-openapi/scripts/omada-api.sh GET "/sites?pageSize=100&page=1"'
```

For a site-scoped operation, list sites first and use the returned `siteId` in later paths. Use your controller's `/doc.html#/home` and `/v3/api-docs` endpoints for endpoint schemas and discovery.

Read [references/api-usage.md](references/api-usage.md) for setup and verified request patterns.
