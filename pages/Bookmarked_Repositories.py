import streamlit as st

from database.db_functions import add_bookmark_to_db, get_bookmarks_from_db, delete_bookmark_from_db
from database.db_functions import get_chat_history

#---------- TITLE ----------
st.set_page_config(page_title='Bookmarked Repositories')
st.title('Bookmarked Repositories')

st.logo("application/git-issue-hound-logo.png", size='large')

#---------- SIDEBAR ----------
with st.sidebar:
    st.header("Chat History")
    
    chat_histories = get_chat_history()
    
    selected_chat = st.selectbox(
        "Select Previous Chat",
        ["New Chat"] + [f"Chat {i+1}" for i in range(len(chat_histories))],
        key="chat_selector"
    )
    
    if selected_chat != "New Chat":

        if st.button("Load Chat"):
            st.session_state.messages = []
            chat_index = int(selected_chat.split()[-1]) - 1
            st.session_state.messages = chat_histories[chat_index]
            st.rerun()
    
    if st.button("New Chat"):
        st.session_state.messages = []
        st.rerun()

#---------- MAIN ----------
if "bookmarked_repos" not in st.session_state:
    st.session_state.bookmarked_repos = get_bookmarks_from_db(type="repository")

repo_to_add = st.text_input("Add a repository to bookmarks:")
if st.button("Add Bookmark") and repo_to_add:
    st.session_state.bookmarked_repos.append(repo_to_add)
    add_bookmark_to_db(type="repository", website=repo_to_add)
    st.success(f"Added {repo_to_add} to bookmarks.")

st.divider()

st.header("Saved Repositories:")
for i, repo in enumerate(st.session_state.bookmarked_repos):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(repo)
    with col2:
        if st.button("🗑️ Delete", key=f"delete_{i}"):
            st.session_state.bookmarked_repos.pop(i)
            delete_bookmark_from_db(type="repository", website=repo)
            st.rerun()