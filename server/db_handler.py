import os
import flask
import sqlite3

DATABASE_PATH = "db.sqlite3"

def relative_to_absolute(path):
    return os.path.join(os.path.dirname(__file__), path)

def connect_db():
    return sqlite3.connect(relative_to_absolute(DATABASE_PATH))

def get_db_connection():
    return flask.g.db

def query_db(query, args=(), one_row_only=False):
    """
    Perform query on DB, and return rows selected
    :param query: The SQL query to perform
    :param args: Arguments that should be placed in query
    :param one_row_only: Used when only 1 row is returned, will return that row (or None if none returned)
    :return: Rows (or row) selected
    """
    cursor = get_db_connection().execute(query, args)
    rows = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    if one_row_only:
        return rows[0] if rows else None
    else:
        return rows

def insert_db(table_name, parameters):
    """
    Insert values to table
    :param table_name: Name of table
    :param parameters: Dictionary of name and value
    :return: ID of row inserted to
    """
    insert_str = "INSERT INTO {table_name} ({columns}) VALUES ({values})".format(
        table_name=table_name, columns=", ".join(parameters.keys()), values=", ".join('?' * len(parameters)),
    )
    cur = get_db_connection().cursor()
    cur.execute(insert_str, parameters.values())
    get_db_connection().commit()

    # Return the ID of the entry inserted
    return cur.lastrowid

def update_db(table, vals, params, condition):
    update_str = "update {table_name} {data}=? where {cond}".format(table_name=table, data="='?',".join(vals), cond=condition)
    print update_str
    print vals
    print params
    cur = get_db_connection().cursor()
    cur.execute(update_str, params)
    print update_str
