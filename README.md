# CI/CD Jenkins Demo

A small Flask application built, tested, and deployed automatically by a Jenkins pipeline. The project demonstrates a complete CI/CD workflow with three stages — **Build**, **Test**, and **Deploy** — all running on a local Jenkins instance backed by Docker.

## Overview

This is a learning exercise for the Data Engineering scholarship. It exercises the core CI/CD muscles:

- **Source-controlled in Git** — every change is tracked on GitHub.
- **Containerized** — the app runs identically on a laptop, in CI, and in production.
- **Automated pipeline** — clicking *Build Now* in Jenkins triggers a fresh Docker build, runs the test suite inside the new image, then redeploys the running container.
- **Traceable artifacts** — every Jenkins run produces a uniquely tagged image: `ci-cd-jenkins-demo:<BUILD_NUMBER>`.

## Architecture

~~~text
┌──────────────┐   git push    ┌──────────────────────┐
│   Developer  │ ────────────▶     GitHub (main)       
└──────────────┘               └───────────┬──────────┘
                                           │
                                           ▼
                              ┌───────────────────────┐
                              │   Jenkins (LTS)       │
                              │   jenkins-with-docker │
                              │   :8086 on host       │
                              └───────────┬───────────┘
                                          │ /var/run/docker.sock
                                          ▼
                          ┌─────────────────────────────────┐
                          │   Docker Desktop (WSL2 backend) │
                          │                                 │
                          │   Build  →  Test  →  Deploy     │
                          │                                 │
                          │   ci-cd-demo container          │
                          │   :8000 → :5000                 │
                          └────────────────┬────────────────┘
                                           │
                                           ▼
                                ┌──────────────────────┐
                                │   Browser → :8000    │
                                │   Build / Host / UTC │
                                └──────────────────────┘
~~~

Jenkins runs inside a container that has the Docker CLI installed and a bind mount to the host's Docker socket. Pipeline stages that issue `docker build` or `docker run` therefore use the **same Docker Desktop daemon** as local development — no Docker-in-Docker, no nested virtualization.

## Project structure

~~~text
ci-cd-jenkins-demo/
├── app/
│   ├── __init__.py
│   ├── main.py                # Flask app: / renders the status card, /health returns JSON
│   └── templates/
│       └── index.html         # Card UI with build_number / hostname / deployed_at
├── tests/
│   ├── __init__.py
│   └── test_app.py            # pytest using Flask test client
├── screenshots/               # Submission screenshots
├── .dockerignore
├── .gitignore
├── Dockerfile                 # python:3.10-slim, deps + app + tests
├── Jenkinsfile                # Declarative pipeline: Build → Test → Deploy
├── README.md
└── requirements.txt           # flask==3.0.3, pytest==8.3.3
~~~

## How to run locally

Requires **Python 3.10+** and (for the Docker workflow) **Docker Desktop**.

### Option A — virtualenv

~~~bash
cd ci-cd-jenkins-demo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the app on http://127.0.0.1:5000
python -m app.main

# In another terminal, run the tests
pytest -v
~~~

### Option B — Docker

~~~bash
cd ci-cd-jenkins-demo
docker build -t ci-cd-jenkins-demo:local .

# Run tests inside the image
docker run --rm ci-cd-jenkins-demo:local pytest -v

# Run the app on http://127.0.0.1:8000
docker run --rm -d \
  --name ci-cd-demo \
  -e BUILD_NUMBER=local \
  -p 8000:5000 \
  ci-cd-jenkins-demo:local

# Stop it
docker stop ci-cd-demo
~~~

## How to run the pipeline

Prerequisite: a Jenkins instance with the Docker CLI inside the container and the host Docker socket bind-mounted.

1. Open Jenkins at `http://localhost:8086`.
2. **New Item** → name: `ci-cd-jenkins-demo` → type: **Pipeline** → **OK**.
3. In the job configuration, scroll to **Pipeline**:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/IbrahimAbbas-spec/ci-cd-demo.git`
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
4. **Save**, then click **Build Now**.
5. Wait for the **Stage View** to show three green cells (Build / Test / Deploy).
6. Open `http://127.0.0.1:8000` — the status card should display the current Jenkins build number.

## Endpoints

| Method | Path      | Description                                                       |
|--------|-----------|-------------------------------------------------------------------|
| GET    | `/`       | Renders the status card (build number, hostname, UTC start time)  |
| GET    | `/health` | Returns `{"status": "ok", "build": "<BUILD_NUMBER>"}` (HTTP 200)  |

## Screenshots

Both screenshots are full-window captures with the Windows clock visible.

- `screenshots/app-ui.png` — the application card at `http://127.0.0.1:8000` after a successful pipeline run.
- `screenshots/jenkins-stage-view.png` — the Jenkins **Stage View** with all three stages green.

A combined PDF of both screenshots is uploaded to Google Drive as part of the scholarship submission.

## Tech stack

- **Language:** Python 3.10
- **Web framework:** Flask 3.0.3
- **Test framework:** pytest 8.3.3
- **Container runtime:** Docker (Docker Desktop on WSL2)
- **CI/CD:** Jenkins LTS (custom `jenkins-with-docker:lts` image with Docker CLI added)
- **VCS:** Git + GitHub

## Author

**Ibrahim Abbas** — Data Engineering scholarship, 2026.
GitHub: https://github.com/IbrahimAbbas-spec
