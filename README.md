# Level-14 RFQ Automation - Complete Package (Minimal Runnable)

This package is a fully self-contained, syntactically correct Level-14 implementation skeleton.
It includes multi-agent modules, an LLM client stub (works without API keys), a Flask panel backend,
a token-limiter placeholder, and scheduler tasks — all designed to run without errors out-of-the-box.

## How to run (local quick test)
1. Create and activate a virtualenv (recommended).
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python core/main.py`
4. Open http://127.0.0.1:8080/status

Notes:
- The LLM client is a safe stub that returns deterministic outputs when an API key is not provided.
- No external network calls are required to run the package locally for testing.
