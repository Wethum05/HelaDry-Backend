from flask import Blueprint, jsonify, g
from ..middleware.auth_middleware import firebase_required
from ..utils.responses import success, error
from firebase_admin import db

session_bp = Blueprint("session", __name__)


@session_bp.route("/my-sessions", methods=["GET"])
@firebase_required
def get_user_sessions():
    try:
        sessions_ref = db.reference("sessions")
        sessions = sessions_ref.get()

        if not sessions:
            return jsonify(success([])), 200

        user_sessions = [
            session
            for session in sessions.values()
            if session.get("user_id") == g.user_id
        ]

        return jsonify(success(user_sessions)), 200

    except Exception:
        return jsonify(error("Failed to fetch sessions")), 500

@session_bp.route("/sync", methods=["POST"])
@firebase_required
def sync_session_route():
    from ..services.session_service import sync_offline_session
    try:
        data = request.get_json()
        if not data:
            return jsonify(error("Request body is required")), 400

        device_id = data.get("device_id")
        session_data = data.get("session_data", {})
        history_logs = data.get("history_logs", [])

        if not device_id:
            return jsonify(error("device_id is required")), 400

        result = sync_offline_session(g.user_id, device_id, session_data, history_logs)

        if "error" in result:
            return jsonify(error(result["error"])), 500

        return jsonify(success(result)), 200

    except Exception as e:
        return jsonify(error(str(e))), 500
