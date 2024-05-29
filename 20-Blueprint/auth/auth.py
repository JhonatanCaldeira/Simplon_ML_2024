from flask import render_template, request, Blueprint
from models.model_auth import ModelAuth
from . import session

authentication_bp = Blueprint('autentication_bp', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')

@authentication_bp.route('/login')
def login_get():
    return render_template("auth/login.html")

@authentication_bp.route('/login', methods=['POST'])
def login_post():
    if (request.form.get("inputEmail") != "" and 
        request.form.get("inputPassword") != ""):
        auth = {}
        auth["inputEmail"] = request.form.get("inputEmail")
        auth["inputPassword"] = request.form.get("inputPassword")

        user = session.query(ModelAuth).filter_by(
            email=auth["inputEmail"], password=auth["inputPassword"]
            ).first()

        if user:
            return user.username

    return render_template("auth/login.html")

@authentication_bp.route('/register')
def register_get():
    return render_template("auth/register.html")

@authentication_bp.route('/register',methods=['POST'])
def register_post():
    if (request.form.get("username") != "" and 
        request.form.get("password") != "" and
        request.form.get("email") != ""):

        auth = {}
        auth["username"] = request.form.get("username")
        auth["password"] = request.form.get("password")
        auth["email"] = request.form.get("email")

        new_user = ModelAuth(username=auth["username"], 
                            email=auth["email"],
                            password=auth["password"])
        session.add(new_user)
        session.commit()

        return auth
    return render_template("auth/register.html")