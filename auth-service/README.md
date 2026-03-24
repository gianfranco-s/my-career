# Auth Service

Companion microservice for `my-career`. Accepts username and password, returns a signed JWT.
The main API verifies tokens using the shared `JWT_SECRET` — this service is the only one that issues them.

## How it works

- Users are defined at startup via the `USERS` env var — no database.
- Passwords are hashed in memory at startup; plain text never persists.
- `POST /v1/auth/token` returns a Bearer JWT valid for `JWT_TTL_HOURS` (default 24h).

## Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `JWT_SECRET` | yes | — | Shared secret with the main API. Must match. |
| `USERS` | yes | — | Comma-separated `username:password` pairs, e.g. `alice:pass1,bob:pass2` |
| `JWT_TTL_HOURS` | no | `24` | Token lifetime in hours |


## Run with Docker

```bash
docker buildx build -t career-auth-service .

docker run -p 8001:8001 \
  -e JWT_SECRET=0ne-sm4l-st3p-for-m4n \
  -e USERS=admin:pass1,gian:pass2 \
  career-auth-service
```

## Get a token

```bash
curl -X POST http://localhost:8001/v1/auth/token \
  -d "username=alice&password=pass1"
```

Response:
```json
{"access_token": "<jwt>", "token_type": "bearer"}
```

Use the token in requests to the main API:
```bash
curl http://localhost:8080/v1/resume \
  -H "Authorization: Bearer <jwt>"
```
