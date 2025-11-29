from panel_backend.status_route import status_bp
from flask import Blueprint, request, jsonify
from autopilot.decision_engine import AutopilotDecisionEngine
from core.email_engine import email_parser   # FIXED: correct import

panel_bp = Blueprint("panel_backend", __name__)


# ----------------------------------------
# 1) AUTOPILOT DECISION ENGINE ROUTE
# ----------------------------------------
@panel_bp.route("/suggest_action", methods=["POST"])
def suggest_action():
    data = request.json
    parsed_email = data.get("parsed_email")
    rfq_data = data.get("rfq_data")

    engine = AutopilotDecisionEngine()
    result = engine.decide(parsed_email, rfq_data)

    return jsonify(result)


# Register status checker route
panel_bp.register_blueprint(status_bp, url_prefix="/")


# ----------------------------------------
# 2) EMAIL PARSER (NLP Engine) ROUTE
# ----------------------------------------
@panel_bp.route("/parse_email", methods=["POST"])
def parse_email_route():
    data = request.json
    raw_email = data.get("raw_email", "")

    if not raw_email:
        return jsonify({
            "error": "raw_email missing",
            "parsed": {}
        }), 400

    # Use global parser (safe, no circular imports)
    parsed = email_parser.parse(raw_email)

    return jsonify({
        "parsed": parsed
    })
