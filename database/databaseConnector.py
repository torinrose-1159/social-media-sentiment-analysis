import psycopg2
from psycopg2 import sql
from config import config

def dbConnect(database: str):
    try:
        connection = None
        params = config(database, "database.ini")
        print("Connecting to the postgreSQL database for %s..." %(database))
        connection = psycopg2.connect(**params)
        print("Connection successful!")
        return connection

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

def cursorConnect(connection):
    try:
        print("Creating a SQL query object")
        cursor = connection.cursor()
        print("SQL object creation successful")
        return cursor

    except(Exception) as error:
        print(error)
        return None

def dbDisconnect(connection):
    try:
        print("Disconnecting from postgreSQL database...")
        connection.close()
        print("Database connection terminated.")
    except(Exception) as error:
        print(error)

def cursorDisconnect(cursor):
    try:
        print("Disconnecting cursor object...")
        cursor.close()
        print("Cursor connection terminated.")
    except(Exception) as error:
        print(error)

def insertRecord(cursor, platform, data):
    try:
        print("Attempting to enter a record into the %s database..." %platform)
        if platform == "bluesky":
            query = sql.SQL("""
                            INSERT INTO bluesky_post_data ({columns})
                            VALUES ({values})
                            """).format(
                                columns=sql.SQL(',').join(map(sql.Identifier, data.keys())),
                                values=sql.SQL(',').join([sql.Placeholder()] * len(data))
                            )
            cursor.execute(query, list(data.values()))
            cursor.connection.commit()
            print("Record insertion successful!")
    except(Exception) as error:
        print(error)
        cursor.connection.rollback()