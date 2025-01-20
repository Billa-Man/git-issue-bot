import streamlit as st
import json
from database.functions.connect_database import get_db_connection

#---------- SIDEBAR CHAT HISTORY ----------
def save_chat_history():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            if len(st.session_state.messages) > 1:
                messages = [
                    {
                        'role': message.role,
                        'content': message.content
                    }
                    for message in st.session_state.messages
                ]
                
                json_content = json.dumps(messages)
                
                cursor.execute("""
                    INSERT INTO chat_history (chat)
                    VALUES (%s::jsonb) 
                    ON CONFLICT (chat) DO NOTHING
                """, (json_content,))
                conn.commit()


def get_chat_history():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT chat FROM chat_history ORDER BY timestamp ASC")
        return cursor.fetchall()