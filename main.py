from nlp.parser import EmailParser
from flask import Flask
from panel_backend.routes import panel_bp
from panel_ui.routes import ui_bp

def create_app():
    app = Flask(__name__)

    # BACKEND API ROUTES
    app.register_blueprint(panel_bp, url_prefix="/")

    # UI ROUTES
    app.register_blueprint(ui_bp, url_prefix="/ui")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
