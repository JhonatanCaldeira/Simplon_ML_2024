import os
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database

from models.model import Product, Base, Customers, Order

from config.config import DATABASE_HOST, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME
from flask import Flask, request


# Configuration initiale
app = Flask(__name__)
engine = create_engine(f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}")

# Fonctions utilitaires
def ajouter_historique(session_id, prompt, generated_code, execution_result):
    pass
    # historique = Historique(session_id=session_id, prompt=prompt, generated_code=generated_code, execution_result=execution_result)
    # db.session.add(historique)
    # db.session.commit()

def execute_python_code(code: str) -> str:
    output = ""
    try:
        with redirect_stdout(StringIO()) as s:
            exec(code)
            output = s.getvalue()
    except Exception as e:
        output = str(e)
    return output

# Routes
@app.route('/generate', methods=['POST'])
def generate_code():
    prompt = request.json.get("texte", "")
    response = openai.Completion.create(
      model="gpt-3.5-turbo",
      prompt=prompt,
      max_tokens=500
    )
    generated_code = response.choices[0].text.strip()
    ajouter_historique(session_id=request.json.get("session_id"), prompt=prompt, generated_code=generated_code, execution_result="")
    return jsonify({"code": generated_code})

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.json.get("code", "")
    langage = request.json.get("langage", "")
    output = ""
    if langage == "python":
        output = execute_python_code(code)
    ajouter_historique(session_id=request.json.get("session_id"), prompt="", generated_code=code, execution_result=output)
    return jsonify({"output": output})

@app.route('/get_history', methods=['POST'])
def get_history():
    session_id = request.json.get("session_id", "")
    historique = Historique.query.filter_by(session_id=session_id).order_by(Historique.timestamp.desc()).all()
    return jsonify([{"prompt": h.prompt, "code": h.generated_code, "result": h.execution_result} for h in historique])

# Exécution
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
