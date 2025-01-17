import streamlit as st

st.header("Manage Bookmarked Repositories")
if "bookmarked_repos" not in st.session_state:
    st.session_state.bookmarked_repos = []

repo_to_add = st.text_input("Add a repository to bookmarks:")
if st.button("Add Bookmark") and repo_to_add:
    st.session_state.bookmarked_repos.append(repo_to_add)
    st.success(f"Added {repo_to_add} to bookmarks.")

#---------- Sidebar ----------

if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_button_label(chat_id, first_message):
    return f"Chat {chat_id}: {' '.join(first_message.split()[:5])}..."

with st.sidebar:
    st.header("Chat History")
    for chat_id, chat in enumerate(st.session_state.chat_history):
        button_label = get_button_label(chat_id, chat["first_message"])
        if st.button(button_label):
            st.session_state.current_chat = chat["messages"]

    st.divider()

    st.header("Bookmarked Repositories:")
    for repo in st.session_state.bookmarked_repos:
        st.write(repo)