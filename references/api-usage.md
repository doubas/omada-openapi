# API usage

## Environment

The wrapper loads `OMADA_URL`, `OMADA_CLIENT`, and `OMADA_SECRET` from the nearest workspace `.env`. Use an HTTPS controller base URL without a trailing slash.

## Verified flow

1. Run the wrapper without arguments to check controller reachability.
2. List sites with pagination:

   ```bash
   bash -lc 'bash .agents/skills/omada-openapi/scripts/omada-api.sh GET "/sites?pageSize=100&page=1"'
   ```

3. Use the returned `siteId` for scoped endpoints:

   ```bash
   bash -lc 'bash .agents/skills/omada-openapi/scripts/omada-api.sh GET "/sites/{siteId}/devices?pageSize=100&page=1"'
   bash -lc 'bash .agents/skills/omada-openapi/scripts/omada-api.sh GET "/sites/{siteId}/clients?pageSize=100&page=1"'
   ```

## Discovery

- Online documentation: `${OMADA_URL}/doc.html#/home`
- OpenAPI specification: `GET /v3/api-docs`
- API token header: `Authorization: AccessToken=<token>`
