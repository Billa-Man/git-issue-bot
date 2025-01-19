import streamlit as st
import pandas as pd
from loguru import logger

from application.functions import get_button_label
from database.db_functions import get_top_repositories

#---------- TITLE ----------
st.set_page_config(page_title='Top Repositories')
st.title('Top Repositories')

language_filter = st.selectbox(
    "Select Language",
    ["All", "Python", "JavaScript", "Java", "Go"]
)

#---------- DATABASE ----------
top_repos = get_top_repositories(language_filter)

#---------- PROCESS AND DISPLAY REPOS ----------
if top_repos:

    data = []
    for repo in top_repos:
        data.append({
            "repo_name": repo["name"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "language": repo["language"],
        })

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

else:
    st.warning("No repositories to display.")

#---------- SIDEBAR ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("Chat History")
    for chat_id, chat in enumerate(st.session_state.chat_history):
        button_label = get_button_label(chat_id, chat["first_message"])
        if st.button(button_label):
            st.session_state.current_chat = chat["messages"]
