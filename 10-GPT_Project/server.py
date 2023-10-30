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
engine = create_engine(f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}")

# Méthode responsable pour enregistrer une requête dans le database
def save_history(language, question, code):
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        obj_langage = session.query(Langage.id_langage).filter_by(langage=language).first()
        textecode = TexteCode(id_langage=obj_langage.id_langage, texte=question, code=code)
        session.add(textecode)
        session.commit()
        code_id = textecode.id
    return code_id


def update_history(code_id, code):
    Session = sessionmaker(bind=engine)
    
    with Session.begin() as session:
        update_code = session.query(TexteCode).filter_by(id=code_id).first()

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
    except Exception as e:
        output = f"Erreur lors de l'exécution: {str(e)}"
    finally:
        update_history(code_id, code)
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
    with sessionmaker(bind=engine).begin() as session:
        result_query = session.query(Langage.langage).all()
        langage_json = json.dumps(','.join([lan.langage for lan in result_query]))
     
    return langage_json

# Route responsable pour lister tout l'historique stocké dans la base de données
@app.route("/api/getHistoryList")
def get_history_list():
    with sessionmaker(bind=engine).begin() as session:
        lst_obj_texte = session.query(
            TexteCode.id,
            TexteCode.texte
            ).order_by(TexteCode.id.desc()).all()

        texte_json = json.dumps(
            [(texte.id, texte.texte) for texte in lst_obj_texte])
    
    return texte_json

@app.route("/api/getHistoryByCode")
def get_history_by_code():
    code_id = request.args.get("code_id")
    with sessionmaker(bind=engine).begin() as session:
        lst_obj_texte = session.query(
            TexteCode.id,
            TexteCode.texte,
            TexteCode.code,
            Langage.langage).join(
                TexteCode, TexteCode.id_langage == Langage.id_langage
            ).filter_by(id=code_id).order_by(TexteCode.id.desc()).all()

        texte_json = json.dumps(
            [(texte.id, texte.texte, 
            texte.code, texte.langage) for texte in lst_obj_texte])
        
    print('HISTORY',texte_json)
    return texte_json

# Route responsable pour envoyer la question demandé par l'utilisateur à OPEN AI.
@app.route("/api/openai")
def openai_request():
    openai.api_key = OPENAI_API_KEY

    language = request.args.get("language")
    question = request.args.get("question")

    assistant_type = f"{language} developper"
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": " I want you to act as a senior " + assistant_type + " You only answer with fenced code block without further explanations."},
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
    # for i in json.loads(openai_request()):
    #     print('ID', i[0])
    #     print('CODE', i[1])
    # print(get_language())
    # save_history()
    # for i in json.loads(get_history()):
    #     print('teste', i[0])
    # save_history('python', 'test', 'test')