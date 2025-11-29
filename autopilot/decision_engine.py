from core.token_manager import add_token_usage
from autopilot.action_types import ActionType


class AutopilotDecisionEngine:

    def decide(self, email: dict, rfq: dict):
        """
        Level-14 Autopilot Decision Engine
        
        email: parsed_email from NLP engine
        rfq: RFQ metadata or live record
        """

        # -------------------------
        # REAL TOKEN COUNT SIMULATION
        # Replace later with actual NLP token usage
        # -------------------------
        simulated_tokens = self._estimate_tokens(email, rfq)
        add_token_usage(simulated_tokens)

        # -------------------------
        # Decision logic starts here
        # -------------------------
        if not email:
            return {
                "action": ActionType.NO_ACTION,
                "reason": "No email data received"
            }

        category = email.get("category")
        status = rfq.get("status") if rfq else None
        vendor_delay = rfq.get("vendor_delay_days") if rfq else None

        # 1. Vendor sent quotation → Mark quotation received
        if category == "quotation" and status == "open":
            return {
                "action": ActionType.MARK_QUOTATION_RECEIVED,
                "reason": "Vendor sent quotation"
            }

        # 2. Vendor too late → Send reminder
        if vendor_delay and vendor_delay > 2:
            return {
                "action": ActionType.SEND_VENDOR_REMINDER,
                "reason": "Vendor delayed more than 2 days"
            }

        # 3. Nothing strong → no action
        return {
            "action": ActionType.NO_ACTION,
            "reason": "No strong decision"
        }

    # ------------------------------------------------------
    # INTERNAL TOKEN ESTIMATOR (temporary — improves later)
    # ------------------------------------------------------
    def _estimate_tokens(self, email: dict, rfq: dict):
        """
        Temporary token estimation until Level-10 NLP integration.

        email and rfq are small → token estimate:
        - 20 tokens base
        - +1 per 10 characters of text fields
        """

        if not email:
            return 10

        text = ""

        # Collect all string fields in email
        for v in email.values():
            if isinstance(v, str):
                text += v

        # Include RFQ fields too
        for v in (rfq or {}).values():
            if isinstance(v, str):
                text += v

        length = len(text)
        extra = max(1, length // 10)

        return 20 + extra
