"""Tests for the Flask app's HTTP endpoints.

Uses Flask's built-in test client — no real HTTP server is started.
Fast, deterministic, and safe to run inside the Jenkins Test stage.
"""

from app.main import app


def test_index_returns_200_and_renders_title():
    """GET / should return 200 and the rendered page must include the H1 title."""
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    # The template index.html contains: <h1>CI/CD Jenkins Demo</h1>
    assert "CI/CD Jenkins Demo" in body


def test_health_returns_ok_json():
    """GET /health should return JSON with status=ok and a build key."""
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.is_json
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert "build" in payload