import streamlit as st
from pymongo import MongoClient
import pprint

st.sidebar.markdown('Connexion à une Base de Données NoSQL (MongoDB)')
st.title('Connexion à une Base de Données NoSQL (MongoDB)')

name = st.text_input('Name: ')
email = st.text_input('E-mail: ')

col1, col2, _, _ = st.columns([1,1,1,1])
with col1:
    btn_insert = st.button('Save new User')

with col2:
    btn_del = st.button('Delete User')


client = MongoClient()
db = client['mydatabase']
utilisateurs = db['utilisateurs']

if btn_insert:
    post = {
        "name": name,
        "email": email,
    }
    utilisateurs.insert_one(post)

if btn_del:
    post = {
        "name": name,
        "email": email,
    }
    utilisateurs.delete_one(post)

for user in utilisateurs.find():
    st.write(user)

client.close()