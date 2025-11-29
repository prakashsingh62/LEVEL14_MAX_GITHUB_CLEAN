from alerts.alert_manager import alert_async
from core.stats_collector import stats

class VendorAgent:

    def next_action(self, rfq):
        try:
            stats.increment("vendor_checks")

            days = rfq.get("last_vendor_response_days", 0)
            rfq_id = rfq.get("id", "unknown")

            if days >= 3:
                alert_async(f"⏳ Vendor Delay: RFQ {rfq_id} no reply for {days} days.")
                stats.increment("vendor_delayed")
                return {
                    "action": "escalate",
                    "reason": f"Vendor silent for {days} days"
                }

            return {
                "action": "no_action",
                "reason": "Vendor within acceptable timeline"
            }

        except Exception as e:
            alert_async(f"🏭 VendorAgent Error: {str(e)}")
            stats.increment("vendor_agent_errors")
            return {"action": "no_action", "reason": "VendorAgent error"}
