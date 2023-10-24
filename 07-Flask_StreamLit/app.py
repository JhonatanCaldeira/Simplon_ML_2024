import streamlit as st
import pandas as pd
import requests

BASE_URL = "http://localhost:5000"

labels = requests.get(f"{BASE_URL}/api/labels").json()
selector = st.multiselect("Select: ", labels)

st.write(selector)

if selector:
    selected_values = ''
    for key, value in enumerate(selector):
        selected_values += value + ','

    df = pd.read_json(
        requests.get(f"{BASE_URL}/api/data", params={"selector": selected_values[:-1]}).json()
    )

    st.dataframe(df)

