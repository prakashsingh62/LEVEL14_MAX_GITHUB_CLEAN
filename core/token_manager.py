import json, os, threading
from datetime import datetime
from alerts.alert_manager import alert_async
from core.stats_collector import stats

TOKEN_FILE = "token_usage.json"
_lock = threading.Lock()

def _safe_load():
    if not os.path.exists(TOKEN_FILE):
        return {"today_cost": 0}
    try:
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    except Exception:
        alert_async("🔥 Token file corrupted — resetting.")
        return {"today_cost": 0}

def _safe_save(data):
    try:
        with _lock:
            with open(TOKEN_FILE, "w") as f:
                json.dump(data, f)
    except Exception as e:
        alert_async(f"🔥 Failed to write token file: {str(e)}")

def update_cost(amount):
    data = _safe_load()
    data["today_cost"] = data.get("today_cost", 0) + amount
    _safe_save(data)
    if data["today_cost"] > 50:
        alert_async(f"⚠️ High LLM cost today: ₹{data['today_cost']}")
    stats.increment("llm_cost_updates")

def get_today_cost():
    data = _safe_load()
    return data.get("today_cost", 0)

def reset_daily_cost():
    _safe_save({"today_cost": 0})
    stats.increment("llm_cost_resets")
