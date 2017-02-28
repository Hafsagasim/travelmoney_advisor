import pickle
import lreg_forecaster as fc
from datetime import timedelta
from flask import Flask, jsonify, request, Response, make_response,  current_app
from functools import update_wrapper

app = Flask(__name__)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

#return the available currencies
@app.route("/currencies", methods=['GET'])
@crossdomain(origin='*')
def get_currencies():
   return jsonify(fc.currencies), 200


#expecting : { "currency" : "EUR", "days": 5} format
@app.route("/forecast", methods=['POST', 'GET'])
@crossdomain(origin='*')
def call_forecaster():
    if not request.json or not 'currency' in request.json:
        abort(4)
    currency = request.json['currency']
    forecast_out = int(request.json['days'])
    return jsonify(fc.lin_reg_predict(currency, forecast_out, save_ds = True,savemodel = True, silent = False, cache = False,
                    train_a_lot = 1, retrain = False, refresh_interval = 1)), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0')