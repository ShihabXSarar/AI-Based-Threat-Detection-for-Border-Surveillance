from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

# Determine important paths
package_dir = os.path.dirname(os.path.abspath(__file__))  # falcon_ai/app
falcon_root = os.path.dirname(package_dir)  # falcon_ai
project_root = os.path.dirname(falcon_root)  # repo root
templates_dir = os.path.join(project_root, 'templates')
static_dir = os.path.join(project_root, 'static')

from ..config import Config

# Initialize extensions
mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(
        __name__,
        template_folder=templates_dir,
        static_folder=static_dir,
        static_url_path='/static'
    )
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    mongo.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # Initialize upload folder
    config_class.init_app(app)
    
    # Register blueprints
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from .analytics import bp as analytics_bp
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    
    from .chatbot import bp as chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

    from .upload import bp as upload_bp
    app.register_blueprint(upload_bp, url_prefix='/upload')
    
    # User loader for Flask-Login
    from .auth import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)
    
    return app

