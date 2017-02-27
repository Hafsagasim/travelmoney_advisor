import pickle
import lreg_forecaster as fc
from flask import Flask, jsonify, request

app = Flask(__name__)

#return the available currencies
@app.route("/currencies", methods=['GET'])
def get_currencies():
    return jsonify(fc.currencies)

#expecting : { "currency" : "EUR", "days": 5} format
@app.route("/forecast", methods=['POST', 'GET'])
def call_forecaster():
    if not request.json or not 'currency' in request.json:
        abort(4)
    currency = request.json['currency']
    forecast_out = int(request.json['days'])
    response = fc.lin_reg_predict(currency, forecast_out, save_ds = True,savemodel = True, silent = False, cache = False,
                    train_a_lot = 1, retrain = False, refresh_interval = 1)
    return jsonify(response), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0')