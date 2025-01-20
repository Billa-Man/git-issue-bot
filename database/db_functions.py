import uuid
import psycopg2
import streamlit as st
from psycopg2 import OperationalError
from psycopg2.extras import Json
from langchain.schema import ChatMessage

from settings import settings

#---------- CONNECT DATABASE ----------
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

#---------- RETRIEVE, ADD & DELETE REPOS ----------
def add_bookmark_to_db(type, website, user_id=None):
    conn = get_db_connection()

    with conn.cursor() as cursor:
        if type == "issue":
            query = "INSERT INTO bookmarkedissues (website, user_id) VALUES (%s, %s)"
        elif type == "repository":
            query = "INSERT INTO bookmarkedrepositories (website, user_id) VALUES (%s, %s)"
        cursor.execute(query, (website, user_id))
    conn.commit()

@st.cache_data
def get_bookmarks_from_db(type, user_id=None):
    conn = get_db_connection()

    with conn.cursor() as cursor:
        if user_id:
            if type == "issue":
                query = "SELECT website FROM bookmarkedissues WHERE user_id = %s ORDER BY timestamp DESC"
            elif type == "repository":
                query = "SELECT website FROM bookmarkedrepositories WHERE user_id = %s ORDER BY timestamp DESC"
            cursor.execute(query, (user_id,))
        else:
            if type == "issue":
                query = "SELECT website FROM bookmarkedissues ORDER BY timestamp DESC"
            elif type == "repository":
                query =  "SELECT website FROM bookmarkedrepositories ORDER BY timestamp DESC"
            cursor.execute(query)
        rows = cursor.fetchall()
    return [row[0] for row in rows]


def delete_bookmark_from_db(type, website, user_id=None):
    conn = get_db_connection()

    with conn.cursor() as cursor:
        if type == "issue":
            query = "DELETE FROM bookmarkedissues WHERE website = %s AND user_id = %s"
        elif type == "repository":
            query = "DELETE FROM bookmarkedrepositories WHERE website = %s AND user_id = %s"      
        cursor.execute(query, (website, user_id))
    conn.commit()

#---------- SIDEBAR CHAT HISTORY ----------
def save_chat_history():
    conn = get_db_connection()
    messages = st.session_state.messages
    print("FUNCTION:", messages)
    if len(messages) > 1:
        with conn.cursor() as cursor:
            for message in messages:
                cursor.execute("""
                    INSERT INTO chat_history (role, content)
                    VALUES (%s, %s)
                """, (message.role, message.content))


def get_chat_history():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT role, content FROM chat_history ORDER BY timestamp ASC")
        messages = cursor.fetchall()

        chat_history = [{
            "role": role,
            "content": content,
            "additional_kwargs": {},
            "response_metadata": {}
        } for role, content in messages]

        return chat_history