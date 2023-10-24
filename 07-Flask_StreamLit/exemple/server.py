##########################################################
# to run: FLASK_APP=server.py flask run
##########################################################
import json
from flask import Flask, request

app = Flask(__name__)
import pandas as pd
import numpy as np

train = pd.read_csv(
    "https://raw.githubusercontent.com/pkhetland/Facies-prediction-TIP160/master/datasets/facies_vectors.csv"
)
train = train.rename(columns={"Well Name": "WELL"})


@app.route("/api/data")
def data():
    selector = request.args.get("selector")
    if not selector:
        selector = "SHRIMPLIN"
    # print(selector)
    data = train[train["WELL"].isin([selector])]
    # print(data)
    return json.dumps(data.to_json())


@app.route("/api/labels")
def labels():
    return json.dumps(train.WELL.unique().tolist())