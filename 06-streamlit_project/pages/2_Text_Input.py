import streamlit as st

st.title('Tableau de Bord Simple')
st.sidebar.markdown('# Tableau de Bord Client')

col1, col2 = st.columns(2)

with col1:

    nom_prenom = st.text_input('Nom et Prénom')

    if nom_prenom:
        st.write(f'Bonjour, {nom_prenom}!')

with col2:
    detail = st.checkbox('Montrez les détails')

    if detail:
        st.write('Les détails sont affichés')