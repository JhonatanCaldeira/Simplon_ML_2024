import streamlit as st

st.sidebar.markdown('# Tableau de Bord Simple')

st.title('Tableau de Bord Simple')
if st.button('Cliquez-moi'):
    st.write('Vous avez cliqué sur le bouton !')

age = st.slider('How old are you?', 0, 130, 25)
st.write("I'm ", age, 'years old')