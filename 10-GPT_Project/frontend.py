import streamlit as st
import requests
import uuid
import json
from code_editor import code_editor

if 'code_editor' not in st.session_state:
    st.session_state.code_editor = None

if 'textarea' not in st.session_state:
    st.session_state.textarea = None

if 'history' not in st.session_state:
    st.session_state.history = {}

if 'code_id' not in st.session_state:
    st.session_state.code_id = ''

session_id = st.session_state.get("session_id", None)
if not session_id:
    session_id = str(uuid.uuid4())
    st.session_state.session_id = session_id

with open('components/custom_buttons.json') as json_button_file_alt:
    custom_buttons_alt = json.load(json_button_file_alt)

btn_settings_editor_btns = [{
    "name": "copy",
    "feather": "Copy",
    "hasText": True,
    "alwaysOn": True,
    "commands": ["copyAll"],
    "style": {"top": "0rem", "right": "0.4rem"}
  },{
    "name": "update",
    "feather": "RefreshCw",
    "primary": True,
    "hasText": True,
    "showWithIcon": True,
    "commands": ["submit"],
    "style": {"bottom": "0rem", "right": "0.4rem"}
  }]

height = [19, 22]
language="python"
theme="default"
shortcuts="vscode"
focus=False
wrap=True
btns = custom_buttons_alt

def exec_generer():
    response = requests.get("http://localhost:5000/api/openai", 
                            params={"language":langage, "question":texte}, 
                            json={"session_id": session_id, "texte": texte, "langage": langage})
    openai_return = response.json()
    st.session_state.code_id = openai_return[0]
    st.session_state.code_editor = openai_return[1]

def load_history(texte, code):
    st.session_state.textarea = texte
    st.session_state.code_editor = code

# QUESTION AREA
st.title("Transcompilateur")
texte = st.text_area("Entrez la description du programme:")

list_langage = requests.get("http://localhost:5000/api/getLangage")
langage = st.selectbox("Choisissez un langage de programmation:", 
                       (str(list_langage.json()).split(',')))

generer = st.button("Générer", on_click=exec_generer)

# st.text_area('id', st.session_state.code_id)

# CODE EDITOR
ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}  
response_dict = code_editor(st.session_state.code_editor, height = height, 
                            lang=language, theme=theme, shortcuts=shortcuts, 
                            focus=focus, buttons=btns, props=ace_props, 
                            options={"wrap": wrap})

if response_dict['type'] == "submit" and len(response_dict['id']) != 0:
    code_execution = requests.get("http://localhost:5000/api/execute", 
                                  params={"language":langage, "code":response_dict['text'], "code_id": st.session_state.code_id}, 
                                  json={"session_id": session_id, "texte": texte, "langage": langage})
    
    code_response = code_execution.json()
    st.text_area("Résultats:", code_response)

# SIDEBAR
st.sidebar.subheader("Historique des requêtes")
history_response = requests.get("http://localhost:5000/api/getHistory", json={"session_id": session_id, "texte": texte, "langage": langage})

button_id = 0
for item in history_response.json():
    button_id += 1
    button_key = 'button_' + str(button_id)

    st.session_state.history[button_key] = {
        'prompt': item[0],
        'result': item[1]
    }

    st.sidebar.button(item[0][0:30], on_click=load_history(st.session_state.history[button_key]['prompt'], 
                                                           st.session_state.history[button_key]['result']), key=button_key)
# st.sidebar.radio(label='Historique des requêtes', options=[item[0][:30]for item in history_response.json()])