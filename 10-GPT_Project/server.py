import json
import openai

import os
import sys
import io
import pandas as pd
import js2py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database

from models.model import Base, Langage, TexteCode

from config.config import DATABASE_HOST, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME, OPENAI_API_KEY
from flask import Flask, request

app = Flask(__name__)

# Méthode responsable pour crée la connexion avec le database
def create_connection():
    engine = create_engine(f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}")
    return engine

# Méthode responsable pour enregistrer une requête dans le database
def save_history(language, question, code):
    engine = create_connection()
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        obj_langage = session.query(Langage.id_langage).filter_by(langage=language).first()
        textecode = TexteCode(id_langage=obj_langage.id_langage, texte=question, code=code)
        session.add(textecode)
        session.commit()
        code_id = textecode.id
    return code_id


def update_history(code_id, code):
    engine = create_connection()
    Session = sessionmaker(bind=engine)
    
    with Session.begin() as session:
        update_code = session.query(TexteCode).filter_by(id=code_id).first()
        print('ID:', code_id)
        print('CODE', code)
        if update_code:
            update_code.code = code
            session.add(update_code)

    return True


# Méthode responsable pour executer les commandes python écrites par les utilisateurs
def execute_python(code_id, code):
    try:
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        exec(code)
        output = new_stdout.getvalue()

        update_history(code_id, code)
    except Exception as e:
        output = f"Erreur lors de l'exécution: {str(e)}"
    finally:
        sys.stdout = old_stdout

    return json.dumps(output)

# Méthode responsable pour executer les commandes javascript écrites par les utilisateurs
def execute_js(code):
    # Use js2py to execute the JavaScript code
    context = js2py.EvalJs()
    result = context.execute(code)

    return json.dumps(context.result)

# Route responsable pour lister toutes les langages qui ont été stocké dans le database
@app.route("/api/getLangage")
def get_all_language():
    engine = create_connection()

    with sessionmaker(bind=engine).begin() as session:
        result_query = session.query(Langage.langage).all()
        langage_json = json.dumps(','.join([lan.langage for lan in result_query]))
     
    return langage_json

# Route responsable pour lister tout l'historique stocké dans la base de données
@app.route("/api/getHistory")
def get_history():
    engine = create_connection()
    with sessionmaker(bind=engine).begin() as session:
        lst_obj_texte = session.query(TexteCode.texte,TexteCode.code).order_by(TexteCode.id).all()
        texte_json = json.dumps([(texte.texte, texte.code) for texte in lst_obj_texte])
    
    return texte_json

# Route responsable pour envoyer la question demandé par l'utilisateur à OPEN AI.
@app.route("/api/openai")
def openai_request():
    openai.api_key = OPENAI_API_KEY

    language = request.args.get("language")
    question = request.args.get("question")

    # language = 'python'
    # question = 'criar um script que receba dois números, some o quadrado de cada um e reenvie a soma ao quadrado'

    assistant_type = f"{language} developper"
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a " + assistant_type + " assistant, skilled in providing the optimal solution"},
        {"role": "user", "content": question}
    ]
    )

    # print(completion.choices[0].message.content)
    code = str(completion.choices[0].message.content).split("```")[1].split('\n')
    code.pop(0) # Remove the language string
    code = '\n'.join(code)

    code_id = save_history(language, question, code)

    return json.dumps([code_id,code])

# Route responsable pour executer les codes informé par l'utilisateur
@app.route("/api/execute")
def execute_code():
    language = request.args.get("language")
    code = request.args.get("code")
    code_id = request.args.get("code_id")
    
    if language == 'python':
        return execute_python(code_id, code)
    elif language == 'javascript':
        return json.dumps('Under construction :-)')
    else:
        return json.dumps('Unknown Language')

if __name__ == '__main__':
    # print(json.loads(openai_request()))
    for i in json.loads(openai_request()):
        print('ID', i[0])
        print('CODE', i[1])
    # print(get_language())
    # save_history()
    # for i in json.loads(get_history()):
    #     print('teste', i[0])
    # save_history('python', 'test', 'test')