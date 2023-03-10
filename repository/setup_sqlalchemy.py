import os
from sqlalchemy import create_engine

sql_engine = None

def connect():
    # host = os.environ['DB_HOST']
    # port = os.environ['DB_PORT']
    # user = os.environ['DB_USERNAME']
    # password = os.environ['DB_PASSWORD']

    host = 'postgresql'
    port = '5432'
    user = 'username'
    password = 'password'

    url = f'postgresql://{user}:{password}@{host}:{port}/feizi'
    return create_engine(url)

if sql_engine is None:
    sql_engine = connect()
