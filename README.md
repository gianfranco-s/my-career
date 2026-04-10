# My Career - 

Self-hosted (mostly) project, to keep track of my work experience.
* Source of truth is a JSON file, commited to the repo
* Work experience can be managed via Python, although preferred way is by updating the JSON
* Ability to filter by predefined role types
* Backend is designed by using ports and adapters architecture

**[DONE] Stage 1 (Design)**: domain implementation. Export selected work-experience (filtered or otherwise) to pdf  
**[DONE] Stage 2 (AI)**: adapt selected work-experience to specific JobDescription. Generate cover letter based on a selected work-experience and a specific JobDescription  
**[DONE] Stage 3 (API)**: implement HTTP API to return roles, and filtered work experience. PDF needs to be able to be downloaded.  
**[DONE] Stage 4 (Security&Errors)**: add authentication and authorization with JWT. Implement error handling and uniform responses  
Stage 5 (AI over API): implement AI routes  
Stage 6 (Cache): implement local cache for specific requests  

## Run locally
```bash
export OPENAI_API_KEY="<api-key>" \
export JWT_SECRET="0ne-sm4l-st3p-for-m4n" \
uv run uvicorn my_career.adapters.api.app:app --reload --app-dir src
```

### Companion auth service
Handles JWT issuance. Must be running for authenticated requests to work.
```bash
docker compose -f auth-service/docker-compose.yml up --build
curl -X POST http://localhost:8001/v1/auth/token \
  -d "username=gian&password=pass2"
# Additional info at auth-service/README.md
```


## Run dockerized
### Build images

```bash
docker buildx build -f docker/Dockerfile -t my-career:v0.1.0 .
docker buildx build -f auth-service/Dockerfile -t career-auth-service:v0.1.0 auth-service/
```

### Start containers
```bash
docker compose -f docker/docker-compose.yml up
```

## Download PDF resume
```sh
curl -X 'GET' \
  'http://localhost:8000/v1/resume/pdf?role=python-dev' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <token>' \
  -o resume.pdf
```
