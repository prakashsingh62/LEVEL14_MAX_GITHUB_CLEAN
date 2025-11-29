from alerts.alert_manager import alert_async
from core.stats_collector import stats
from .llm_client import LLMClient
import time

class EmailParser:
    def parse(self, text):
        start = time.time()
        client = LLMClient()
        try:
            stats.increment("parsed_emails")
            result = client.parse_email(text)
            duration = (time.time() - start)
            if duration > 5:
                alert_async(f"⚠️ Slow email parsing: {duration:.2f}s")
            return result
        except Exception as e:
            alert_async(f"🔎 Email Parse Error: {str(e)}")
            stats.increment("parser_errors")
            return {"type": "unknown", "entities": {}, "raw": text}
