from flask import Flask

# Routes
from .routes import AuthRoutes, CompaniesRoutes, ImagenRoutes

app = Flask(__name__)

def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Register Blueprints
    app.register_blueprint(AuthRoutes.main, url_prefix='/auth')
    app.register_blueprint(CompaniesRoutes.main, url_prefix='/companies')
    app.register_blueprint(ImagenRoutes.main, url_prefix='/upload')

    return app
