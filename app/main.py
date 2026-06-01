"""Minimal Flask app used to demonstrate a Jenkins CI/CD pipeline.

Exposes a single route that renders a small status page showing the
build number, container hostname, and deployment time. These values
let us visually confirm that the deployed container is the one Jenkins
just built and pushed.
"""

import os
import socket
from datetime import datetime, timezone

from flask import Flask, render_template

# Create the Flask application instance
app = Flask(__name__)

# Capture deployment metadata once at startup
BUILD_NUMBER = os.environ.get("BUILD_NUMBER", "local-dev")
HOSTNAME = socket.gethostname()
DEPLOYED_AT = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


@app.route("/")
def index():
    """Render the main status page."""
    return render_template(
        "index.html",
        build_number=BUILD_NUMBER,
        hostname=HOSTNAME,
        deployed_at=DEPLOYED_AT,
    )


@app.route("/health")
def health():
    """Lightweight health check used by tests and Docker."""
    return {"status": "ok", "build": BUILD_NUMBER}, 200


if __name__ == "__main__":
    # Bind to all interfaces so the container is reachable from the host
    app.run(host="0.0.0.0", port=5000)