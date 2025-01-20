import psycopg2
from psycopg2 import OperationalError

from settings import settings

#---------- CONNECT TO DATABASE ----------
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="mydatabase",
            user="postgres",
            password=settings.POSTGRES_PASSWORD,
            host="db",
            port=5432
        )
        return conn
    except OperationalError as e:
        print(f"Error: Unable to connect to the database. Details: {e}")
        return None