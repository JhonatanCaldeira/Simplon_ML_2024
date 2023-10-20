import sounddevice as sd
import numpy as np 
import matplotlib.pyplot as plt
import streamlit as st

st.title('Visualisation de Signaux Sinusoïdaux')
st.sidebar.markdown('# Visualisation de Signaux Sinusoïdaux')

f = st.slider('Pick une fréquence',0, 1000, 440)

N = 1
t = np.linspace(0,1)
x = np.sin(2 * np.pi * f * t)

st.line_chart(x)