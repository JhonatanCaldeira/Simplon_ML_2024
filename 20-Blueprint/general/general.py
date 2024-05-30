from flask import render_template, request, Blueprint
from flask_login import login_required, login_user, logout_user, current_user


general_bp = Blueprint('general_bp', __name__,
                       template_folder='templates',
                       static_folder='static')

@general_bp.route("/index")
@login_required
def index():
    return render_template("general/index.html", name=current_user.username)

@general_bp.route("/about")
def about():
    return render_template("general/about.html")
