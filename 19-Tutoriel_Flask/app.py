from flask import Flask 
from routes.routes import routes_setup

app = Flask(__name__)
routes_setup(app)

if __name__ == "__main__":
    app.run(debug=True)
