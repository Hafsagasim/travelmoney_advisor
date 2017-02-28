import pickle
import lreg_forecaster as fc
from datetime import timedelta
from flask import Flask, jsonify, request, Response, make_response,  current_app
from functools import update_wrapper
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#return the available currencies
@app.route("/currencies", methods=['GET'])
def get_currencies():
    response = jsonify(fc.currencies), 200
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['content-type'] = "application/json"
    return response

#expecting : { "currency" : "EUR", "days": 5} format
@app.route("/forecast", methods=['POST', 'GET'])
def call_forecaster():
    if not request.json or not 'currency' in request.json:
        abort(4)
    currency = request.json['currency']
    forecast_out = int(request.json['days'])

    response = jsonify(fc.lin_reg_predict(currency, forecast_out, save_ds=True, savemodel=True, silent=False, cache=False,
                                       train_a_lot=1, retrain=False, refresh_interval=1)), 201
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['content-type'] = "application/json"
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')