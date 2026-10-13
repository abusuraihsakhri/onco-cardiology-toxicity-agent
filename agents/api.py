"""
FastAPI REST API Server for Onco Cardiology Toxicity Agent.
"""
from typing import Dict, Any, List, Optional
import os
import hmac
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from .base import AuditLogger, PHIGuard, SecurityException
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Onco Cardiology Toxicity Agent API",
    description="Synthetic-data rule demonstrator; not for clinical decisions.",
    version="3.0.0-ENTERPRISE",
)


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "onco-cardiology-toxicity-agent", "domain": "Illustrative rule demonstration", "standard": "Not clinically validated", "version": "3.0.0-ENTERPRISE"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "system_status": "NOMINAL_OPTIMAL"
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    try:
        dossier = supervisor.process_task(payload)
        return dossier.to_dict()
    except SecurityException as e:
        raise HTTPException(status_code=400, detail=f"Security violation: {str(e)}")


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except SecurityException:
        raise HTTPException(status_code=400, detail="Request contains a potential identifier")


@app.get("/api/audit/logs")
def api_audit_logs(x_audit_token: Optional[str] = Header(default=None)):
    """Restrict ledger access to an explicitly configured read token."""
    expected = os.getenv("AUDIT_LOG_READ_TOKEN")
    if not expected:
        raise HTTPException(status_code=404, detail="Audit log access is disabled")
    if not x_audit_token or not hmac.compare_digest(x_audit_token, expected):
        raise HTTPException(status_code=403, detail="Invalid audit log token")
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
