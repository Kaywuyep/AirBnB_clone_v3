#!/usr/bin/python3
"""lets start our api"""
from flask import Flask
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(obj):
    """ calls methods close() to end session """
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """Handles 404 error"""
    return ({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host=host, port=port, threaded=True)
