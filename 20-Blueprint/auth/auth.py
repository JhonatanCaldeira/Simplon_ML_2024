from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from models.user import User, db

authentication_bp = Blueprint('autentication_bp', __name__,
    template_folder='templates',
    static_folder='static')

@authentication_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':

        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return render_template("general/profile.html", name=user.username)
        else:
            flash('Invalid password provided', 'error')
            return render_template("auth/login.html")
    
    return render_template("auth/login.html")

@authentication_bp.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        if (request.form.get("username") != "" and 
            request.form.get("password") != "" and
            request.form.get("email") != ""):
            
            username = request.form.get("username")
            password = request.form.get("password")
            email = request.form.get("email")

            new_user = User(username=username, 
                                email=email)
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()

            if new_user:
                return new_user.username
        
    return render_template("auth/register.html")

@authentication_bp.route('/forgot_password', methods=['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        if (request.form.get("email") != ""):
            email = request.form.get("email")
            user = User.query.filter_by(email=email)

            if user:
                flash('Link to reset the password has been sent to you e-mail box', 'error')
                return render_template("auth/login.html")
    return render_template("auth/forgot_password.html")

@authentication_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('autentication_bp.login'))