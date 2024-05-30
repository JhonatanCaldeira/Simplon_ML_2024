from flask import Flask
from flask_login import LoginManager
from models import db
from general.general import general_bp
from auth.auth import authentication_bp
from models.user import User   

login_manager = LoginManager()
login_manager.login_view = 'autentication_bp.login'

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"

    db.init_app(app)
    login_manager.init_app(app)
        
    app.register_blueprint(general_bp)
    app.register_blueprint(authentication_bp)
    
    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
