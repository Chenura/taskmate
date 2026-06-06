"""Register all route blueprints."""

from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.notes import notes_bp
from routes.reminders import reminders_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(reminders_bp)

    # Main dashboard route
    from flask import render_template
    from flask_login import login_required
    from datetime import datetime, timezone

    @app.context_processor
    def inject_now():
        return {"now": datetime.now(timezone.utc).replace(tzinfo=None)}

    @app.route("/")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

    # Debug endpoint - remove after fixing
    @app.route("/debug/db")
    def debug_db():
        from flask import jsonify
        from app import db
        import traceback, sys
        try:
            from models import Task, Note, Reminder
            db.create_all()
            return jsonify({"status": "ok", "tables": "created"})
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "python": sys.version,
            })
