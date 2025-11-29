import time
from alerts.alert_manager import alert_async
from alerts.daily_summary import send_daily_summary
from core.stats_collector import collect_stats
from core.token_manager import get_today_cost
from agents.vendor_agent import VendorAgent
from agents.client_agent import ClientAgent
from alerts.rfq_stuck import rfq_stuck_alert
from alerts.cost_alerts import cost_alert

vendor_agent = VendorAgent()
client_agent = ClientAgent()

def scan_vendor_delays(rfqs):
    try:
        for rfq in rfqs:
            days = rfq.get("last_vendor_response_days", 0)
            if days >= 3:
                vendor_agent.next_action(rfq)
    except Exception as e:
        alert_async(f"🔥 Vendor Delay Scan Error: {str(e)}")

def scan_stuck_rfqs(rfqs):
    try:
        for rfq in rfqs:
            if rfq.get("stuck", False):
                rfq_stuck_alert(rfq.get("id"), rfq.get("status"))
    except Exception as e:
        alert_async(f"🔥 RFQ Stuck Scan Error: {str(e)}")

def check_llm_cost():
    try:
        today_cost = get_today_cost()
        cost_alert(today_cost)
    except Exception as e:
        alert_async(f"🔥 LLM Cost Scan Error: {str(e)}")

def maintenance_cleanup():
    try:
        pass
    except Exception as e:
        alert_async(f"🧹 Cleanup Error: {str(e)}")

def auto_recovery():
    try:
        pass
    except Exception as e:
        alert_async(f"🔁 Auto-recovery failure: {str(e)}")

def run_daily_summary():
    try:
        stats = collect_stats()
        send_daily_summary(stats)
    except Exception as e:
        alert_async(f"🔥 Daily Summary Error: {str(e)}")

def daily_run(load_rfqs):
    try:
        rfqs = load_rfqs()
        run_daily_summary()
        scan_vendor_delays(rfqs)
        scan_stuck_rfqs(rfqs)
        check_llm_cost()
        maintenance_cleanup()
        auto_recovery()
        return "max_daily_tasks_completed"
    except Exception as e:
        alert_async(f"🔥 Scheduler Fatal Error: {str(e)}")
        return "scheduler_error"
