import json
import os
import threading
from datetime import datetime
from alerts.alert_manager import alert_async

STATS_FILE = "system_stats.json"
_lock = threading.Lock()

def _default_stats():
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "emails_processed": 0,
        "emails_parsed": 0,
        "email_agent_errors": 0,
        "email_engine_errors": 0,
        "parsed_emails": 0,
        "parser_errors": 0,
        "llm_calls": 0,
        "llm_errors": 0,
        "llm_cost_updates": 0,
        "llm_cost_resets": 0,
        "vendor_checks": 0,
        "vendor_delayed": 0,
        "vendor_agent_errors": 0,
        "client_checks": 0,
        "client_pending": 0,
        "client_agent_errors": 0,
        "decisions_made": 0,
        "actions_completed": 0,
        "scheduler_runs": 0,
        "recovery_events": 0
    }

def _safe_load():
    if not os.path.exists(STATS_FILE):
        return _default_stats()
    try:
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        alert_async("🔥 Stats file corrupted — resetting.")
        return _default_stats()

def _safe_save(data):
    try:
        with _lock:
            with open(STATS_FILE, "w") as f:
                json.dump(data, f, indent=2)
    except Exception as e:
        alert_async(f"🔥 Failed to write stats file: {str(e)}")

def increment(key):
    data = _safe_load()
    if key not in data:
        data[key] = 0
    data[key] += 1
    _safe_save(data)

def collect_stats():
    stats = _safe_load()
    return {
        "total_rfq": stats.get("emails_processed", 0),
        "vendor_pending": stats.get("vendor_delayed", 0),
        "client_pending": stats.get("client_pending", 0),
        "overdue": stats.get("parser_errors", 0),
        "email_errors": stats.get("email_agent_errors", 0),
        "llm_errors": stats.get("llm_errors", 0),
        "success_today": stats.get("actions_completed", 0)
    }

def reset_daily():
    _safe_save(_default_stats())
    alert_async("♻️ Daily stats reset performed.")
