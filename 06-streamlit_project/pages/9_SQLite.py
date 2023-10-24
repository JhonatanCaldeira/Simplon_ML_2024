import streamlit as st
import pandas as pd
import sqlite3
import os
import sys

st.title('Connexion à une Base de Données SQL (SQLite)')
st.sidebar.markdown('Connexion à une Base de Données SQL (SQLite)')

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'data')
DB_FILE = os.path.join(DATA_DIR,'database.db')

try:
    con = sqlite3.connect(DB_FILE)
except Exception as e:
    st.write('Connection Failure: ', e)
    sys.exit()

try:
    cursor = con.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100),
                email VARCHAR(200))
    """)
    con.commit()
except Exception as e:
    st.write('Create table failed: ', e)
    con.close()
    sys.exit()

name = st.text_input('Name: ')
email = st.text_input('E-mail: ')
btn_insert = st.button('Save new User')

if btn_insert:
    try:
        cursor.execute("""
                INSERT INTO utilisateurs (name, email) VALUES (?,?)
        """, [name,email])
        con.commit()
    except Exception as e:
        st.write('Error during insertion: ', e)
        con.rollback()

try:
    cursor.execute("""
        SELECT DISTINCT id, name, email FROM utilisateurs
    """)
    st.dataframe(pd.DataFrame(cursor.fetchall(), columns=['id','Name','Email']))
except Exception as e:
    st.write(e)

con.close()