import gzip
import json

import flask
from connexion.apps.flask_app import FlaskJSONEncoder
from flask import Response, jsonify, request


app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def gzip_json_response(data):
    # Reuse Connexion's encoder (Decimal, date, datetime) so this shared helper
    # stays compatible with normal API JSON responses.
    payload = json.dumps(data, cls=FlaskJSONEncoder, separators=(',', ':')).encode('utf-8')
    response = Response(gzip.compress(payload, compresslevel=6), mimetype='application/json')
    response.headers['Content-Encoding'] = 'gzip'
    return response


@app.errorhandler(400)
def bad_request(error=None):
    if error is None:
        error = {
            'error': 'Bad Request: ' + request.url,
        }
    resp = jsonify(error)
    resp.status_code = 400

    return resp


@app.errorhandler(403)
def forbidden(error=None):
    if error is None:
        error = {
            'error': 'Forbidden: ' + request.url,
        }
    resp = jsonify(error)
    resp.status_code = 403

    return resp


@app.errorhandler(404)
def not_found(error=None):
    if error is None:
        error = {'error': 'Not Found: ' + request.url}
    resp = jsonify(error)
    resp.status_code = 404

    return resp


@app.errorhandler(415)
def unsupported_media_type(error=None):
    if error is None:
        error = {
            'error': 'Unsupported media type: ' + request.url,
        }
    resp = jsonify(error)
    resp.status_code = 415

    return resp


@app.errorhandler(500)
def internal_server_error(error=None):
    if error is None:
        error = {
            'error': 'Internal Server Error: ' + request.url,
        }
    resp = jsonify(error)
    resp.status_code = 500

    return resp


@app.errorhandler(501)
def not_implemented(error=None):
    if error is None:
        error = {
            'error': 'Not Implemented: ' + request.url,
        }
    resp = jsonify(error)
    resp.status_code = 501

    return resp
