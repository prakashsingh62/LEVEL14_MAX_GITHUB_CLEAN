from alerts.alert_manager import alert_async
from core.stats_collector import stats
from core.email_engine import safe_parse
import time

class EmailAgent:

    def read_and_parse(self, raw_email, sender, subject, body, attachments):
        start = time.time()
        try:
            stats.increment("emails_processed")

            parsed = safe_parse(
                raw=raw_email,
                sender=sender,
                subject=subject,
                body=body,
                attachments=attachments
            )

            duration = time.time() - start
            if duration > 4:
                alert_async(f"⚠️ Slow email parsing in EmailAgent: {duration:.2f}s")

            return parsed

        except Exception as e:
            alert_async(f"📩 EmailAgent Failure: {str(e)}")
            stats.increment("email_agent_errors")

            return {
                "type": "unknown",
                "raw": raw_email,
                "sender": sender,
                "subject": subject,
                "body": body,
                "attachments": attachments
            }
