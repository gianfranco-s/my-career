# My Career - 

Self-hosted (mostly) project, to keep track of my work experience.
* Source of truth is a JSON file, commited to the repo
* Work experience can be managed via Python, although preferred way is by updating the JSON
* Ability to filter by predefined role types
* Backend is designed by using ports and adapters architecture

Iteration 1 (Design): domain implementation. Export selected work-experience (filtered or otherwise) to pdf
TO DO:
* improve ports and adapters for pdf exporter
* move convert_to_pdf to an adapter, to avoid mixing responsibilities. We should have a port/adapter in charge of performing the export

Iteration 2 (AI): adapt selected work-experience to specific JobDescription. Generate cover letter based on a selected work-experience and a specific JobDescription
Iteration 3 (API): implement HTTP API to return roles, and filtered work experience. Iterate over FastAPI, Flask, maybe Django
Iteration 4 (Security): add authentication and authorization with JWT
Iteration 5 (Cache): implement local cache for specific requests
