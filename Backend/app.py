from flask import Flask, jsonify
import os

# Using relative imports assuming this is a package structure
from .config import Config
from .extensions import init_firebase

from .routes.device_routes import device_bp
from .routes.session_routes import session_bp
from .routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    try:
        # Initialize Firebase using the flexible credentials logic
        init_firebase(
            app.config["FIREBASE_CREDENTIALS"],
            app.config["FIREBASE_DATABASE_URL"]
        )
    except Exception as e:
        # Logs the error but allows the app to start so you can see the error in Render logs
        print(f"CRITICAL ERROR: Failed to initialize Firebase: {str(e)}")

    # Register Blueprints
    app.register_blueprint(device_bp, url_prefix="/device")
    app.register_blueprint(session_bp, url_prefix="/session")
    app.register_blueprint(user_bp, url_prefix="/user")

    @app.route("/")
    def health_check():
        return jsonify({
            "status": "running",
            "service": "HelaDry Backend",
            "environment": "production" if not app.config["DEBUG"] else "development"
        }), 200

    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    return app

# Expose 'app' for Gunicorn (Render's production server)
app = create_app()

if __name__ == "__main__":
    # Use Render's dynamic port, default to 5000 for local safety
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])