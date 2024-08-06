import psycopg2
import json

with open('dbprop.json') as config_file:
    DATABASE = json.load(config_file)


def get_db_connection():
    conn = psycopg2.connect(
        host=DATABASE['host'],
        database=DATABASE['database'],
        user=DATABASE['user'],
        password=DATABASE['password']
    )
    return conn

