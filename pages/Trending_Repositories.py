import streamlit as st
import pandas as pd
from loguru import logger

from application.functions import get_button_label
from database.db_functions import get_db_connection

#---------- TITLE ----------
st.set_page_config(page_title='Trending Repositories')
st.title('Trending Repositories')

st.header("Filters")
language_filter = st.selectbox(
    "Select Language",
    ["All", "Python", "JavaScript", "Java", "Go"]
)

#---------- DATABASE ----------
conn = get_db_connection()

query = """
    SELECT repo_name, description, stars, forks, language 
    FROM Repositories 
    WHERE (%s = 'All' OR language = %s)
    ORDER BY stars DESC
"""

logger.info(f"Connection: {conn}")

df = pd.read_sql(query, conn, params=[language_filter, language_filter])


st.dataframe(df, use_container_width=True)

st.metric("Total Repositories", len(df))
if len(df) > 0:
    st.metric("Most Stars", df['stars'].max())
    st.metric("Most Forks", df['forks'].max())

#---------- SIDEBAR ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("Chat History")
    for chat_id, chat in enumerate(st.session_state.chat_history):
        button_label = get_button_label(chat_id, chat["first_message"])
        if st.button(button_label):
            st.session_state.current_chat = chat["messages"]
