#!/usr/bin/python3

import MySQLdb
import os

"""
For a single database query
"""
def execute_single_with_parameters(query, parameters):
    database_host = os.environ["NLAB_MYSQL_DATABASE_HOST"]
    database_user = os.environ["NLAB_MYSQL_DATABASE_USER"]
    database_password = os.environ["NLAB_MYSQL_DATABASE_PASSWORD"]
    database_name = os.environ["NLAB_MYSQL_DATABASE_NAME"]
    database_connection = MySQLdb.connect(
        host = database_host,
        user = database_user,
        password= database_password,
        db = database_name,
        charset = "utf8",
        use_unicode = True)
    cursor = database_connection.cursor()
    try:
        cursor.execute(query, parameters)
        results = cursor.fetchall()
        database_connection.commit()
    except MySQLdb.Error as e:
        database_connection.rollback()
        raise e
    finally:
        cursor.close()
        database_connection.close()
    return results
