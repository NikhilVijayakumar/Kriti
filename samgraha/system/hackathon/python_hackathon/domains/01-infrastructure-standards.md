# 01. Infrastructure Standards

**Domain:** Infrastructure
**Audit Target:** `uv.lock`, `Dockerfile`, `docker-compose.yaml`

## Standard Definition
The project must demonstrate reproducible infrastructure. Even if the project is simple, it must use modern Python dependency management (uv) to lock dependencies and optionally provide a containerized execution environment.

### Expected Evidence
1. **Dependency Locking:** A `uv.lock` file must exist at the root.
2. **Containerization:** A `Dockerfile` should be provided to ensure local and offline execution capabilities.
