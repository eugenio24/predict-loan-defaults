from flask import Flask
from flask import render_template, jsonify, request

from sklearn.base import BaseEstimator

from config import Config
from utils import load_model, parse_request

app = Flask(__name__)
app.config.from_object(Config())

model = load_model(app.config['GDRIVE_MODEL_DOWNLOAD_ID'], app.debug)
if model is None or not isinstance(model, BaseEstimator):
    raise ValueError("The loaded model is not a valid scikit-learn model.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict-default", methods=['POST'])
def predict_default():

    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!', 415

    json = request.json
    
    input = parse_request(json)

    if input is None: 
        response = {'error': "Bad Request, error parsing request params."}
        return jsonify(response), 400    

    prediction = model.predict(input.reshape(1, -1))[0]    

    response = {'give_loan': not bool(prediction)} # prediction == 1 => default => no loan
    return jsonify(response)