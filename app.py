from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from models import User  # noqa

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        from routes import register_blueprints
        register_blueprints(app)

        from models import Task, Note, Reminder  # noqa
        try:
            db.create_all()
            app.logger.info("Database tables created/verified")
        except Exception as e:
            import traceback
            app.logger.error(f"DB init failed: {e}")
            app.logger.error(traceback.format_exc())

    return app
