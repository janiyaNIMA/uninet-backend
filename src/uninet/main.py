import os
import sys
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Ensure src directory is in sys.path for import resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.uninet.config import Config
from src.uninet.models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    CORS(app)
    JWTManager(app)

    # Register Route Blueprints
    from src.uninet.routes.auth import auth_bp
    from src.uninet.routes.analytics import analytics_bp
    from src.uninet.routes.excom import excom_bp
    from src.uninet.routes.feed import feed_bp
    from src.uninet.routes.portfolio import portfolio_bp
    from src.uninet.routes.profile import profile_bp
    from src.uninet.routes.recruitment import recruitment_bp
    from src.uninet.routes.settings import settings_bp
    from src.uninet.routes.societies import societies_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(analytics_bp, url_prefix='/api/v1/analytics')
    app.register_blueprint(excom_bp, url_prefix='/api/v1/excom')
    app.register_blueprint(feed_bp, url_prefix='/api/v1/feed')
    app.register_blueprint(portfolio_bp, url_prefix='/api/v1/portfolio')
    app.register_blueprint(profile_bp, url_prefix='/api/v1/profile')
    app.register_blueprint(recruitment_bp, url_prefix='/api/v1/recruitment')
    app.register_blueprint(settings_bp, url_prefix='/api/v1/settings')
    app.register_blueprint(societies_bp, url_prefix='/api/v1/societies')

    @app.route('/health')
    def health_check():
        return {"status": "ok", "service": "uninet-backend"}

    # Ensure all Neon PostgreSQL tables exist (data seeded via run_seed.py)
    with app.app_context():
        db.create_all()

    return app


app = create_app()


def main():
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()

