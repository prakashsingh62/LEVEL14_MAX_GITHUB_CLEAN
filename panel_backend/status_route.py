from flask import Blueprint, jsonify
import datetime
from core.token_manager import get_token_usage


status_bp = Blueprint("status_bp", __name__)


@status_bp.route("/status", methods=["GET"])
def status():
    """
    Returns:
      - pythonpath (for debugging)
      - server status
      - current server time
    """
    return jsonify({
        "pythonpath": __import__("sys").path[0],
        "status": "online",
        "time": datetime.datetime.now().isoformat()
    })


@status_bp.route("/tokens", methods=["GET"])
def tokens():
    """
    Returns real-time token usage from token_usage.json.
    """
    used, remaining = get_token_usage()

    return jsonify({
        "used_tokens": used,
        "remaining_tokens": remaining
    })
