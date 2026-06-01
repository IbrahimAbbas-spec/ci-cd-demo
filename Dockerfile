# syntax=docker/dockerfile:1.6

# Small, predictable base. Python 3.10 matches local dev.
FROM python:3.10-slim

# Behave well in containers and CI:
# - no .pyc files on disk
# - unbuffered stdout/stderr so Jenkins logs stream live
# - no pip cache to keep the image small
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install dependencies first so this layer is cached when only source changes.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application source and tests.
# Tests are included so the Jenkins Test stage can run `pytest` inside this same image.
COPY app/ ./app/
COPY tests/ ./tests/

# Flask app listens on 5000 (see app/main.py).
EXPOSE 5000

# Same entrypoint as local development: python -m app.main
CMD ["python", "-m", "app.main"]