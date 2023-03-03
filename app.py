#!/usr/bin/env python3

import os

from flask import Flask, request, jsonify

app = Flask( __name__ )

@app.route( "/healthz" )
def health():
    return jsonify({ 'status': 'healthy' })
