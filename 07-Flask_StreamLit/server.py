from flask import Flask, request
import json
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('data/GlobalLandTemperaturesByCity.csv')
df.rename(columns={"dt":"Date"},inplace=True)

@app.route("/api/data")
def get_data():
    selector = request.args.get("selector")
    #dt,AverageTemperature,AverageTemperatureUncertainty,City,Country,Latitude,Longitude
    if not selector:
        selector = ["AverageTemperature","City"]
    
    #print(selector)
    data = df[list(selector.split(","))]
    return json.dumps(data.to_json())


@app.route("/api/labels")
def labels():
    return json.dumps(df.columns.to_list())