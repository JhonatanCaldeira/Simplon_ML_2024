import streamlit as st
import json
import requests
import uuid
from code_editor import code_editor

if 'code_editor' not in st.session_state:
    st.session_state.code_editor = None

if 'response_code' not in st.session_state:
    st.session_state.response_code = None

def execute():
    st.session_state.response_code = st.session_state.code_editor

code = False
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

st.title("Transcompilateur")

# User input
texte = st.text_area("Entrez la description du programme:")

# list_langage = requests.get("http://localhost:5000/api/getLangage")
langage = st.selectbox("Choisissez un langage de programmation:", ['python'])

session_id = st.session_state.get("session_id", None)
if not session_id:
    session_id = str(uuid.uuid4())
    st.session_state.session_id = session_id

generer = st.button("Générer")

if generer:
    response = """def calcular_soma_quadrados(num1, num2):
    soma = num1**2 + num2**2
    soma_ao_quadrado = soma**2
    return soma_ao_quadrado

    numero1 = int(input("Digite o primeiro número: "))
    numero2 = int(input("Digite o segundo número: "))

    resultado = calcular_soma_quadrados(numero1, numero2)
    print("A soma ao quadrado dos números é:", resultado)
    """
    code = response
    st.session_state.code_editor = code

ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}  
response_dict = code_editor(st.session_state.code_editor, height = height, lang=language, theme=theme, shortcuts=shortcuts, focus=focus, buttons=btns, props=ace_props, options={"wrap": wrap})

if response_dict['type'] == "submit" and len(response_dict['id']) != 0:
    st.write(response_dict)

