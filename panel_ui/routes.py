from flask import Blueprint, send_from_directory
import os

ui_bp = Blueprint("ui_bp", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@ui_bp.route("/dashboard")
def dashboard_page():
    return send_from_directory(BASE_DIR, "dashboard.html")

@ui_bp.route("/rfq")
def rfq_page():
    return send_from_directory(BASE_DIR, "rfq.html")

@ui_bp.route("/autopilot")
def autopilot_page():
    return send_from_directory(BASE_DIR, "autopilot.html")

@ui_bp.route("/settings")
def settings_page():
    return send_from_directory(BASE_DIR, "settings.html")

@ui_bp.route("/")
def index_page():
    return send_from_directory(BASE_DIR, "index.html")
