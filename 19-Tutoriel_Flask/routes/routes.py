# routes/routes.py 
from flask import render_template, request
from modules.create_session import create_db
from models.model_blog import ModelBlog
from models.model_auth import ModelAuth

session = create_db()

def routes_setup(app):
    @app.route('/')
    def index():
       return render_template("index.html")
    
    @app.route('/login')
    def login_get():
        return render_template("login.html")
    
    @app.route('/login', methods=['POST'])
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
    
        return render_template("login.html")

    @app.route('/register')
    def register_get():
        return render_template("register.html")

    @app.route('/register',methods=['POST'])
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
        return render_template("register.html")

    @app.route('/about')
    def about():
        return render_template("about.html")
 
    # @app.route('/template/demain')
    # def demain():
        
    #     # créer ou vérifier que la base de données existe
    #     req = session.query(ModelBlog).all()
    #     return render_template("page3.html", comments=req)
