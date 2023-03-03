#!/usr/bin/env python3

import os

from flask import Flask, request, jsonify

from repository.setup_sqlalchemy import sql_engine
from repository.user import UserRepository

app = Flask( __name__ )

@app.route("/healthz")
def health():
    passwd = os.environ['DB_PASSWORD']
    return jsonify({'status': 'healthy', 'password': passwd})

@app.route("/all_users")
def all_users():
    user_repo = UserRepository(sql_engine)
    lst = user_repo.all()
    return jsonify(lst)
