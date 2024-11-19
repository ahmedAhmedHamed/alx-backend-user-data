#!/usr/bin/env python3
"""
main app module
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def home_route():
    """ home path """
    return jsonify({'message': 'Bienvenue'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
