#!/usr/bin/env python3

import logging

logging.basicConfig( level = 'INFO' )
global LOG
LOG = logging.getLogger( 'feizi.backend' )

import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from controllers.user import user_routes
from models.administration import User
from repository.setup_sqlalchemy import sql_engine
from repository.user import UserRepository

app = Flask( __name__ )
CORS(app)

app.register_blueprint( user_routes )

@app.route("/healthz")
def health():
    passwd = os.environ['DB_PASSWORD']
    return jsonify({'status': 'healthy', 'password': passwd})
