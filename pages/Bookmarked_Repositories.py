import streamlit as st
from langchain.schema import ChatMessage

from database.functions.bookmark_functions import add_bookmark_to_db, get_bookmarks_from_db, delete_bookmark_from_db
from database.functions.sidebar_functions import get_chat_history

#---------- TITLE ----------
st.set_page_config(page_title='Bookmarked Repositories')
st.title('Bookmarked Repositories')

st.logo("application/git-issue-hound-logo.png", size='large')

#---------- SIDEBAR ----------
with st.sidebar:
    st.header("Chat History")
    
    chat_histories = get_chat_history()
    
    chat_labels = ["New Chat"]
    for chat in chat_histories:
        first_message = chat[1] if chat[1] else "Untitled Chat"
        truncated_label = first_message[:50] + ("..." if len(first_message) > 50 else "")
        chat_labels.append(truncated_label)
    
    selected_chat = st.selectbox(
        "Select Previous Chat",
        chat_labels,
        key="chat_selector"
    )
    
    if selected_chat != "New Chat":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("New Chat", type="primary", use_container_width=True):
                st.session_state.messages = [ChatMessage(role="assistant", content="Hi, How can I help you?")]
                st.query_params.clear()
                st.switch_page("Home.py")
        with col2:
            if st.button("Load Chat", type="secondary", use_container_width=True):
                chat_index = chat_labels.index(selected_chat) - 1
                loaded_messages = chat_histories[chat_index][0]
                st.session_state.messages = [
                    ChatMessage(
                        role=msg['role'],
                        content=msg['content']
                    ) for msg in loaded_messages
                ]
                st.query_params.clear()
                st.switch_page("Home.py")
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("New Chat", type="primary", use_container_width=True):
                st.session_state.messages = [ChatMessage(role="assistant", content="Hi, How can I help you?")]
                st.query_params.clear()
                st.switch_page("Home.py")

#---------- MAIN ----------
if "bookmarked_repos" not in st.session_state:
    st.session_state.bookmarked_repos = get_bookmarks_from_db(type="repository")

repo_to_add = st.text_input("Add a repository to bookmarks:")
if st.button("Add Bookmark", type="primary") and repo_to_add:
    st.session_state.bookmarked_repos.append(repo_to_add)
    add_bookmark_to_db(type="repository", website=repo_to_add)
    st.success(f"Added {repo_to_add} to bookmarks.")

st.divider()
st.subheader("Saved Repositories:")
bookmarked_repos = get_bookmarks_from_db(type="repository", user_id=None)

for i, repo in enumerate(bookmarked_repos):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(repo)
    with col2:
        if st.button("🗑️ Delete", type="primary", key=f"delete_{i}"):
            delete_bookmark_from_db(type="repository", website=repo)
            st.cache_data.clear()
            st.rerun()