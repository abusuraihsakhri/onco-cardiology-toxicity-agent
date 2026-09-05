# Onco Cardiology Toxicity Agent

> **Domain:** Cardiovascular Medicine & Hemodynamic Analytics
> **Reference Guidelines & Standards:** `AHA/ACC Practice Guidelines & ESC Clinical Standards`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Onco Cardiology Toxicity Agent** is an advanced analytical and computational platform implementing Cumulative Anthracycline & ICI Myocarditis Surveillance. It provides multi-agent clinical decision support for cardio-oncology risk stratification.

---

## ⚙️ Key Capabilities & Algorithmic Modules

### 🔬 Core Algorithmic & Evaluation Engines

- **`Severity`** — dedicated module for severity evaluation and state verification.
- **`DomainKnowledgeRegistry`**: Enterprise domain rules, guideline matrices, and evidence benchmarks.
- **`AgentAlert`** — dedicated module for agent alert evaluation and state verification.
- **`CumulativeDoseTrackerAgent`**: Specialized Sub-Agent 1 for onco-cardiology-toxicity-agent
- **`TroponinKineticsAgent`**: Specialized Sub-Agent 2 for onco-cardiology-toxicity-agent
- **`MyocarditisRiskStratifierAgent`**: Specialized Sub-Agent 3 for onco-cardiology-toxicity-agent

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup
```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/onco-cardiology-toxicity-agent.git
cd onco-cardiology-toxicity-agent

# Install dependencies
pip install fastapi uvicorn pydantic pytest

# Set required environment variable
export AUDIT_SECRET_KEY="your-secure-audit-key-min-16-chars"
```

### Docker Deployment
```bash
# Create .env file with required variables
echo "AUDIT_SECRET_KEY=your-secure-audit-key-min-16-chars" > .env

# Build and run
docker-compose up --build
```

---

## 💻 CLI Quickstart & Usage

### 1. Guided Interactive Mode
```bash
python cli.py
```

### 2. Direct Parameterized Evaluation
```bash
python cli.py --task-id <value> --target <value> --primary <value> --secondary <value>
```

### 3. Available Commands

| Command | Description |
|:--------|:------------|
| `audit` | Run single task evaluation |
| `chat` | System configuration query |
| `batch` | Batch process CSV records |
| `verify-audit` | Verify HMAC audit trail integrity |
| `serve` | Launch FastAPI REST server |

### Parameter Reference
- `--task-id`: Specifies input measurement or parameter value.
- `--target`: Specifies input measurement or parameter value.
- `--primary`: Specifies input measurement or parameter value.
- `--secondary`: Specifies input measurement or parameter value.
- `--critical`: Specifies input measurement or parameter value.
- `--status`: Specifies input measurement or parameter value.
- `--input`: Specifies input measurement or parameter value.
- `--output`: Specifies input measurement or parameter value.

### Input Data Schema

| Field | Description | Requirement |
|:------|:------------|:------------|
| `case_id` | Parameter / observation metric | Required |
| `patient_synthetic_id` | Parameter / observation metric | Required |
| `metric_primary` | Parameter / observation metric | Required |
| `metric_secondary` | Parameter / observation metric | Required |
| `is_stat` | Parameter / observation metric | Required |
| `status_flag` | Parameter / observation metric | Required |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active AST and regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

### Security Requirements

**IMPORTANT:** The `AUDIT_SECRET_KEY` environment variable is required to run this application. This key is used to sign the HMAC-SHA256 audit trail.

```bash
# Minimum 16 characters required
export AUDIT_SECRET_KEY="your-secure-audit-key-min-16-chars"
```

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
# Set test environment variable
export AUDIT_SECRET_KEY="test-audit-secret-key-2026-secure"

# Run all tests
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py --tasks 1000 --concurrency 8
```

### Test Coverage

- **PHI Guard Enforcement:** Validates zero-PHI outbound interceptor
- **Specialized Workers:** Tests all three sub-agent evaluation engines
- **Supervisor Consensus:** Validates multi-agent consensus and audit trail
- **Clinical Module:** Tests clinical decision support components
- **API Endpoints:** Validates FastAPI REST endpoints
- **Enrichment Suite:** Tests domain enrichment features

---

## 🐳 Container Deployment

```bash
docker build -t onco-cardiology-toxicity-agent .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY="your-secure-key" onco-cardiology-toxicity-agent
```

---

## 📁 Project Structure

```
onco-cardiology-toxicity-agent/
├── agents/                          # Enterprise agent modules
│   ├── api.py                       # FastAPI REST API
│   ├── base.py                      # Security, PHI guard, audit trail
│   ├── learning.py                  # Bayesian calibration engine
│   ├── llm_factory.py               # LLM provider factory
│   ├── metrics.py                   # Prometheus metrics
│   ├── models.py                    # Pydantic data models
│   ├── streamer.py                  # WebSocket telemetry
│   ├── supervisor.py                # Multi-agent orchestrator
│   └── workers.py                   # Specialized worker agents
├── onco_cardiology_toxicity_agent/  # Clinical module
│   ├── agents.py                    # Clinical sub-agents
│   ├── cli.py                       # Clinical CLI
│   ├── engine.py                    # Clinical decision engine
│   ├── models.py                    # Clinical data models
│   └── server.py                    # Clinical FastAPI server
├── tests/                           # Test suite
│   ├── test_api.py                  # API endpoint tests
│   ├── test_clinical_module.py      # Clinical module tests
│   ├── test_enrichment.py           # Enrichment tests
│   └── test_onco_cardiology_toxicity_agent.py  # Core tests
├── cli.py                           # Main CLI entry point
├── enrichment.py                    # Domain enrichment features
├── simulator.py                     # High-throughput simulator
├── pyproject.toml                   # Project configuration
├── Dockerfile                       # Container build
└── docker-compose.yml               # Container orchestration
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
