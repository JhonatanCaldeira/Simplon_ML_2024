from flask import Flask 

from auth.auth import authentication_bp

app = Flask(__name__)

app.register_blueprint(authentication_bp, url_prefix='/auth')

if __name__ == "__main__":
    app.run(debug=True)
