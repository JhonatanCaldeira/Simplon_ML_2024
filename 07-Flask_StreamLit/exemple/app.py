##########################################################
# to run: streamlit run main.py
##########################################################
import plotly.express as px
import streamlit as st
import pandas as pd
import requests

# labels
labels = requests.get("http://localhost:5000/api/labels").json()
selector = st.multiselect("Select WELL:", labels)

# load data
data = pd.read_json(
    requests.get("http://localhost:5000/api/data", params={"selector": selector}).json()
)

# setup figure
fig = px.scatter(
    x=data["PHIND"],
    y=data["GR"],
)
st.write(fig)