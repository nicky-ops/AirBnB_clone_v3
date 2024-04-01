#!/usr/bin/python3
"""
flask web application
"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(obj):
    """this method handles the decorator @app.teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''return a json-formatted 404 status code response'''
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
