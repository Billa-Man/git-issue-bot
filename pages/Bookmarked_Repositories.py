import streamlit as st
from application.functions import get_button_label

st.set_page_config(page_title='Bookmarked Repositories')
st.title('Bookmarked Repositories')

if "bookmarked_repos" not in st.session_state:
    st.session_state.bookmarked_repos = []

repo_to_add = st.text_input("Add a repository to bookmarks:")
if st.button("Add Bookmark") and repo_to_add:
    st.session_state.bookmarked_repos.append(repo_to_add)
    st.success(f"Added {repo_to_add} to bookmarks.")

st.divider()

st.header("Saved Repositories:")
for i, repo in enumerate(st.session_state.bookmarked_repos):
    col1, col2 = st.columns([3,1])
    with col1:
        st.write(repo)
    with col2:
        if st.button("Delete", key=f"delete_{i}"):
            st.session_state.bookmarked_repos.pop(i)
            st.rerun()

#---------- Sidebar ----------

if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


with st.sidebar:
    st.header("Chat History")
    for chat_id, chat in enumerate(st.session_state.chat_history):
        button_label = get_button_label(chat_id, chat["first_message"])
        if st.button(button_label):
            st.session_state.current_chat = chat["messages"]

