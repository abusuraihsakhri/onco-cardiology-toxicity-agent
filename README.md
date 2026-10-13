# Onco Cardiology Toxicity Agent

A Python rule-engine repository with a **standalone browser demonstrator**. It includes a FastAPI service, command-line evaluation and CSV batch processing, tests, and a separate legacy clinical-named module.

> **Safety:** The current numeric thresholds are unitless demonstration constants, **not** validated cardiotoxicity criteria. This software must not be used to diagnose, risk-stratify, triage, or treat patients. Use synthetic data only.

## Browser demonstrator

The standalone application is in [web/index.html](web/index.html). Open the file in an up-to-date browser to evaluate illustrative inputs and download a JSON summary. All computation runs locally; the page makes no HTTP API requests, stores no user inputs, and does not generate cryptographic audit records.

A GitHub Pages deployment workflow is included in `.github/workflows/pages.yml`. **A public live application URL has not yet been verified.** GitHub Pages must be enabled with **GitHub Actions** as the build source for this repository before the workflow can publish the page.

The browser view is independent of the Python backend, which GitHub Pages cannot host.

## What the code does

- `agents/workers.py`: three deterministic demonstration rules on a generic primary metric (>25), secondary metric (>12) or manual critical flag, and keyword-based status descriptors.
- `agents/supervisor.py`: combines alerts and records an in-memory HMAC-SHA256 chained audit entry.
- `agents/api.py`: FastAPI endpoints (`/health`, `/metrics`, `/api/audit`, `/api/chat`); `/metrics` returns **JSON**, not Prometheus exposition text.
- `cli.py`: a single evaluation, local status query, CSV batch evaluation, and audit-chain verification.
- `onco_cardiology_toxicity_agent/`: an additional older API/CLI with different demonstration thresholds (>20 and >10). Both implementations are preserved for compatibility. Their outputs are **not interchangeable** and neither is a validated clinical algorithm.
- `onco_cardio_sentinel.py` and `enrichment.py`: separate legacy demonstration utilities.

The names "dose tracker" and "troponin kinetics" do **not** imply the inputs are doxorubicin-equivalent dose, LVEF, ECG findings, or measured cardiac troponin. Those inputs lack the units, assay context, baseline, clinical features and risk framework needed for clinical interpretation.

For actual clinical guidance, consult the [2022 ESC Cardio-Oncology Guidelines](https://www.escardio.org/guidelines/clinical-practice-guidelines/all-esc-practice-guidelines/cardio-oncology/); the repository **does not implement their diagnostic or monitoring recommendations**.

## Install and run

Requires Python 3.9+; tests are run in CI with Python 3.10–3.12.

```bash
git clone https://github.com/abusuraihsakhri/onco-cardiology-toxicity-agent.git
cd onco-cardiology-toxicity-agent
python -m pip install -e ".[server,test]"

# Required for the Python supervisor and API; use a unique, private key.
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"

# Deterministic example, with synthetic identifiers only
onco-cardio-agent audit --task-id EXAMPLE-1 --target SYNTH-1 \
  --primary 28 --secondary 5 --status NOMINAL

# Run local HTTP server
onco-cardio-agent serve --host 127.0.0.1 --port 8000
```

The API documentation is available at `http://127.0.0.1:8000/docs` when the local server is running.

### CSV batch processing

```bash
onco-cardio-agent batch --input input.csv --output results.csv
```

Example input columns:

```csv
task_id,target_identifier,primary_metric,secondary_metric,status_descriptor,is_critical_flag
SYN-001,TEST-01,28,5,NOMINAL,false
SYN-002,TEST-02,10,14,DISCORDANT,true
```

A separate legacy script uses different columns:

```bash
python onco_cardio_sentinel.py batch --input sample.csv --output results.csv
```

## Audit and security limitations

The Python supervisor requires `AUDIT_SECRET_KEY` (minimum 16 characters) for HMAC chaining. Integrity verification recomputes each signature as well as checking chain links. The log is **in memory**: it is neither persistently stored nor guaranteed complete after a process restart. It must not be described as a production-compliant audit system.

The regular-expression identifier detector catches some recognizable identifiers but **cannot de-identify or certify data as HIPAA-compliant**. Do not submit real patient identifiers or other sensitive information. The API returns identifiers supplied in synthetic test requests.

The `/api/audit/logs` endpoint is disabled unless `AUDIT_LOG_READ_TOKEN` is configured. When enabled, callers must provide an `X-Audit-Token` request header with that value. Do not expose either key or token in browser-side source. HTTPS, independent authentication, authorization, durable audit storage, clinical validation, and privacy review are required before any real-world deployment.

The mock chat adapter returns static local text; the provider names in `agents/llm_factory.py` are not functional integrations with external language models.

## Docker

```bash
# Supply a private, randomly generated key in an ignored .env file.
printf 'AUDIT_SECRET_KEY=%s\n' "$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" > .env
docker compose up --build
```

The Docker image runs the FastAPI server on port 8000 and is independent of GitHub Pages.

## Testing

```bash
python -m compileall -q agents onco_cardiology_toxicity_agent cli.py enrichment.py onco_cardio_sentinel.py simulator.py
python -m pytest -q
python simulator.py 100
```

The test suite covers the existing rule outputs, API endpoints, field validation, regex guard, and HMAC tampering detection. These are **software regression tests, not external clinical validation**.

## Technology and license

Python 3.9+, Pydantic 2, FastAPI, Uvicorn, pytest, standard HTML/CSS/JavaScript, Docker, and GitHub Actions. The browser page targets current Chromium, Firefox, and Safari engines and does not require Pyodide or a backend.

Licensed under the [MIT License](LICENSE).
