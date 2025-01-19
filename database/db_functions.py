import json

import psycopg2
from psycopg2 import OperationalError

import streamlit as st
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
def save_chat_to_db(session_id, first_message, messages):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO chat_history (session_id, first_message, messages)
            VALUES (%s, %s, %s)
            RETURNING chat_id
            """,
            (session_id, first_message, json.dumps(messages))
        )
        chat_id = cur.fetchone()[0]
        conn.commit()
        return chat_id
    finally:
        cur.close()
        conn.close()

def load_chat_history(session_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT chat_id, first_message, messages 
            FROM chat_history 
            WHERE session_id = %s 
            ORDER BY created_at DESC
            """,
            (session_id,)
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

#---------- SAVE CHAT TO CHAT HISTORY ----------
def save_current_chat():
    if st.session_state.chat_history:
        current_chat = st.session_state.chat_history[-1]
        save_chat_to_db(
            st.session_state.session_id,
            current_chat["first_message"],
            current_chat["messages"]
        )