import streamlit as st

from database.functions.bookmark_functions import add_bookmark_to_db, get_bookmarks_from_db, delete_bookmark_from_db
from database.functions.sidebar_functions import get_chat_history

#---------- TITLE ----------
st.set_page_config(page_title='Bookmarked Issues')
st.title('Bookmarked Issues')

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
if "bookmarked_issues" not in st.session_state:
    st.session_state.bookmarked_issues = get_bookmarks_from_db(type="issue")

issue_to_add = st.text_input("Add an issue to bookmarks:")
if st.button("Add Bookmark") and issue_to_add:
    st.session_state.bookmarked_issues.append(issue_to_add)
    add_bookmark_to_db(type="issue", website=issue_to_add)
    st.success(f"Added {issue_to_add} to bookmarks.")

st.divider()

st.subheader("Saved Issues:")
bookmarked_issues = get_bookmarks_from_db(type="issue", user_id=None)

for i, issue in enumerate(bookmarked_issues):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(issue)
    with col2:
        if st.button("🗑️ Delete", key=f"delete_{i}"):
            delete_bookmark_from_db(type="issue", website=issue)
            st.cache_data.clear()
            st.rerun()

