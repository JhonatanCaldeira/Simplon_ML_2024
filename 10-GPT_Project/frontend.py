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

if 'language' not in st.session_state:
    st.session_state.language = 'python'

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

def load_history(code_id=''):
    history_response = requests.get("http://localhost:5000/api/getHistoryByCode",  params={"code_id": code_id}).json()
    code_id, texte, code, language = history_response[0]

    st.session_state.code_id = code_id
    st.session_state.textarea = texte
    st.session_state.code_editor = code
    st.session_state.language = language

def reset_form():
    st.session_state.code_id = ''
    st.session_state.textarea = ''
    st.session_state.code_editor = ''
    st.session_state.language = ''

# QUESTION AREA
st.title("Transcompilateur")
texte = st.text_input("Entrez la description du programme:", value=st.session_state.textarea)

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
history_response = requests.get("http://localhost:5000/api/getHistoryList", json={"session_id": session_id, "texte": texte, "langage": langage})

buttonstyle = '''
<style>
    div[data-testid="stSidebarUserContent"] .stButton > button {
        width: calc(100%);
        text-align: start;
        display: block;
        float:left;
    }
    div[data-testid="stSidebarUserContent"] .stButton > button p {
        font-size: 0.8rem;
    }
</style>
'''
st.markdown(buttonstyle, unsafe_allow_html=True)

st.sidebar.button('Nouvelle', on_click=reset_form)

for i, item in enumerate(history_response.json()):
    st.sidebar.button(item[1][0:30], key=i, on_click=load_history, args=(item[0],))