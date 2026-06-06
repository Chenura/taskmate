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

    @app.route("/")
    @login_required
    def dashboard():
        return render_template("dashboard.html")
