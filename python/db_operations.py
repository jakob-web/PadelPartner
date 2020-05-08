from config import *
import psycopg2

def connectToDb():
    connection = psycopg2.connect( 
    dbname=dbname, 
    user=user,
    password=password,
    host=host)
    return connection

def closeConnections(cursor, connection):
    cursor.close()
    connection.close()

def fetchone(query, val):
    result = dbExecute(query, "fetchone", val)
    return result

def fetchall(query, val):
    result = dbExecute(query, "fetchall", val)
    return result

def fetchmany(query, val):
    result = dbExecute(query, "fetchmany", val)
    return result

def update(query, val):
    dbExecute(query, "", val)

def insert(query, val):
    dbExecute(query, "", val)
    

def dbExecute(query, fetch, val):
    connection = connectToDb()
    cursor = connection.cursor()
    if val != "":
        cursor.execute(query, val)
    else:
        cursor.execute(query)
    result = ""
    if fetch != "":
        if fetch == "fetchone":
            result = cursor.fetchone()
        elif fetch == "fetchall":
            result = cursor.fetchall()
        elif fetch == "fetchmany":
            result = cursor.fetchmany()
    elif val != "":
        connection.commit()
    closeConnections(cursor, connection)
    return result
