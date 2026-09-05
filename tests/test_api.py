"""
Automated Pytest Test Suite for the FastAPI REST API endpoints.
"""
import os
import sys
from pathlib import Path

# Set required environment variable before importing agents
os.environ.setdefault("AUDIT_SECRET_KEY", "test-audit-secret-key-2026-secure")

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


def test_health_endpoint():
    """Test the health endpoint returns expected structure."""
    from agents.api import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert "service" in data


def test_metrics_endpoint():
    """Test the metrics endpoint returns expected structure."""
    from agents.api import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "dossiers_processed_total" in data
    assert "audit_blocks_total" in data


def test_audit_endpoint():
    """Test the audit endpoint processes payload correctly."""
    from agents.api import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    payload = {
        "task_id": "API-TEST-01",
        "target_identifier": "TARGET-API-01",
        "primary_metric": 35.0,
        "secondary_metric": 15.0,
        "status_descriptor": "DISCORDANT",
        "is_critical_flag": True,
    }
    response = client.post("/api/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == "API-TEST-01"
    assert data["overall_urgency"] == "CRITICAL_STAT_PANIC"
    assert data["total_alerts"] > 0
    assert "audit_hash" in data


def test_audit_endpoint_nominal():
    """Test the audit endpoint with nominal values."""
    from agents.api import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    payload = {
        "task_id": "API-TEST-02",
        "target_identifier": "TARGET-API-02",
        "primary_metric": 10.0,
        "secondary_metric": 5.0,
        "status_descriptor": "NOMINAL",
        "is_critical_flag": False,
    }
    response = client.post("/api/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["overall_urgency"] == "ROUTINE"
    assert data["integrity_status"] == "VALIDATED_OPTIMAL"


def test_chat_endpoint():
    """Test the chat endpoint returns a response."""
    from agents.api import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.post("/api/chat", json={"query": "What is the system status?"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data


def test_audit_logs_endpoint():
    """Test the audit logs endpoint returns trail data."""
    from agents.api import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.get("/api/audit/logs")
    assert response.status_code == 200
    data = response.json()
    assert "audit_trail" in data
    assert "verified" in data


def test_phi_guard_api():
    """Test that PHI guard blocks requests with PHI."""
    from agents.api import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    payload = {
        "task_id": "Patient John Doe MRN-994827",
        "target_identifier": "TARGET-API-03",
        "primary_metric": 10.0,
        "secondary_metric": 5.0,
        "status_descriptor": "NOMINAL",
    }
    response = client.post("/api/audit", json=payload)
    # Should be rejected due to PHI
    assert response.status_code == 400 or response.status_code == 500


def test_clinical_api_health():
    """Test the clinical module API health endpoint."""
    from onco_cardiology_toxicity_agent.server import create_app

    app = create_app()
    if app is None:
        pytest.skip("FastAPI not installed")

    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"


def test_clinical_api_audit():
    """Test the clinical module API audit endpoint."""
    from onco_cardiology_toxicity_agent.server import create_app

    app = create_app()
    if app is None:
        pytest.skip("FastAPI not installed")

    from fastapi.testclient import TestClient
    client = TestClient(app)
    payload = {
        "case_id": "API-CLIN-01",
        "patient_synthetic_id": "SYN-API-01",
        "primary_metric": 35.0,
        "secondary_metric": 15.0,
        "status_flag": "DISCORDANT",
        "is_stat": True,
    }
    response = client.post("/api/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == "API-CLIN-01"
    assert data["total_alerts"] > 0
