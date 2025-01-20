import streamlit as st
from database.functions.connect_database import get_db_connection

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
                    ON CONFLICT (content) DO NOTHING
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