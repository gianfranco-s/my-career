# My Career - 

Self-hosted (mostly) project, to keep track of my work experience.
* Source of truth is a JSON file, commited to the repo
* Work experience can be managed via Python, although preferred way is by updating the JSON
* Ability to filter by predefined role types
* Backend is designed by using ports and adapters architecture

**[DONE] Iteration 1 (Design)**: domain implementation. Export selected work-experience (filtered or otherwise) to pdf  
**[DONE] Iteration 2 (AI)**: adapt selected work-experience to specific JobDescription. Generate cover letter based on a selected work-experience and a specific JobDescription  
**Iteration 3 (API)**: implement HTTP API to return roles, and filtered work experience. Iterate over FastAPI, Flask, maybe Django. PDF needs to be able to be downloaded.  
Iteration 4 (Security): add authentication and authorization with JWT  
Iteration 5 (AI over API): implement AI routes  
Iteration 6 (Cache): implement local cache for specific requests  
