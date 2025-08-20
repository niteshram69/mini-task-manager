from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from datetime import datetime

db = SQLAlchemy()
bootstrap = Bootstrap()
csrf = CSRFProtect()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    
    db.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    

    @app.context_processor
    def inject_now():
        return {'current_year': datetime.utcnow().year}
    
   
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    
    with app.app_context():
        db.create_all()
    
    return app
