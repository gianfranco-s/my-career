## v0.1.0

### Added
* [Adapter] Expose AI tailoring over HTTP
* [Tests] Test cases for change management

## v0.0.4

### Changed
* Use pydantic-settings to define global configs

### Added
* [Auth] JWT auth
* [Errors] Centralized error handling
* [CompanionAuthService] External auth service, used to create JWT
* [Health] Simple health endpoint


## v0.0.3

### Added
* [Adapter] FastAPI to expose resume, roles, filters, pdf downloads
* [UseCases] Domain-like functions to avoid having FastAPI instantiate the domain


## v0.0.2

### Added
* [Domain] Read JSON with cover letter
* [Adapter] Export cover letter to pdf file
* [Adapter] Tailor resume and cover letter to specific Job Description


## v0.0.1

### Added
* [Domain] Read JSON with resume
* [Domain] Filter, based on predifined roles
* [Adapter] Export to pdf file
* Logging config
* Environment variables config
