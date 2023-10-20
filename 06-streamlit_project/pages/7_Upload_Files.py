import streamlit as st
import pandas as pd

st.title('Lecture et Affichage de Données')
st.sidebar.markdown('# Lecture et Affichage de Données')

type = st.sidebar.radio('Type de Fichier',["CSV","JSON","EXCEL"])

if type == 'CSV':
    
    st.header("Lecture de données depuis un fichier CSV")
    uploaded_file = st.file_uploader("Choose a file",type='csv')

    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)

elif type == 'JSON':
    st.header("Lecture de données depuis un fichier JSON")
    uploaded_file = st.file_uploader("Choose a file",type='json')

    if uploaded_file is not None:
        dataframe = pd.read_json(uploaded_file,orient='records')
        st.write(dataframe)
else:
    st.header("Lecture de données depuis un fichier EXCEL")