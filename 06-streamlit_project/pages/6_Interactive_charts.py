import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Graphique interactif')
st.sidebar.markdown('# Graphique interactif')

tab_bar, tab_circle = st.tabs(['Graphique à Barres','Graphique Circulaire'])

with tab_bar:
    st.title("Graphique à barres interactif")
    n_category = st.slider('N de catégories',0, 10, 5)
    n_values = st.slider('N de valeurs',0, 10, 5)

    chart_data = pd.DataFrame(np.random.randn(n_values, n_category), columns=[i for i in range(n_category)])

    st.bar_chart(chart_data)

with tab_circle:
    st.title("Graphique Circulaire")
    frequency = st.slider('Frequence', min_value=0.0, max_value=3.0, value=1.0, step=0.05, key='frequency')
    strength = st.slider('Force', 0, 7, 3, key='strength')

    df = px.data.wind()
    df = df[df['frequency'] <= frequency]

    if strength == 0:
        strength = ['0-1']
    elif strength == 1:
        strength = ['0-1','1-2']
    elif strength == 2:
        strength = ['1-2','2-3']
    elif strength == 3:
        strength = ['2-3','3-4']
    elif strength == 4:
        strength = ['3-4','4-5']
    elif strength == 5:
        strength = ['4-5','5-6']
    elif strength == 6:
        strength = ['5-6','6+']      
    else:
         strength = ['0-1','1-2','2-3','3-4','4-5','4-5','5-6','6+']

    df = df[df['strength'].isin(strength)]
    
    fig = px.line_polar(df, r="frequency", theta="direction", color="strength", line_close=True,
                        color_discrete_sequence=px.colors.sequential.Plasma_r,
                        template="plotly_dark",)

    st.plotly_chart(fig, theme=None, use_container_width=True)