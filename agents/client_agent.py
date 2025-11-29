from alerts.alert_manager import alert_async
from core.stats_collector import stats

class ClientAgent:

    def next_action(self, rfq):
        try:
            stats.increment("client_checks")

            rfq_id = rfq.get("id", "unknown")
            status = rfq.get("status", "")
            days = rfq.get("client_pending_days", 0)

            if status == "awaiting_client" and days >= 2:
                alert_async(f"👤 Client Pending: RFQ {rfq_id} awaiting approval for {days} days.")
                stats.increment("client_pending")
                return {
                    "action": "remind_client",
                    "reason": "Client pending 2+ days"
                }

            return {
                "action": "no_action",
                "reason": "No client action required"
            }

        except Exception as e:
            alert_async(f"👤 ClientAgent Error: {str(e)}")
            stats.increment("client_agent_errors")
            return {"action": "no_action", "reason": "ClientAgent error"}
