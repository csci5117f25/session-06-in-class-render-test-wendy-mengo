from flask import Flask, current_app, g
import os
import psycopg2

from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

from contextlib import contextmanager
import logging

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require')
    
@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)
        
@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

def add_person(name, msg):
    with get_db_cursor(True) as cur:
        cur.execute("INSERT INTO people (name, msg) values (%s, %s)", [name, msg])
        
def get_people():
    retval = []
    with get_db_cursor(False) as cur:
        with get_db_cursor() as cur:
            cur.execute("select * from people")
            for row in cur: retval.append({"name": row["name"], "msg": row["msg"]})
    return retval
