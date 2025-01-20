import streamlit as st

from database.db_functions import add_bookmark_to_db, get_bookmarks_from_db, delete_bookmark_from_db
from database.db_functions import get_chat_history

#---------- TITLE ----------
st.set_page_config(page_title='Bookmarked Issues')
st.title('Bookmarked Issues')

st.logo("application/git-issue-hound-logo.png", size='large')

#---------- SIDEBAR ----------


#---------- MAIN ----------
if "bookmarked_issues" not in st.session_state:
    st.session_state.bookmarked_issues = get_bookmarks_from_db(type="issue")

issue_to_add = st.text_input("Add an issue to bookmarks:")
if st.button("Add Bookmark") and issue_to_add:
    st.session_state.bookmarked_issues.append(issue_to_add)
    add_bookmark_to_db(type="issue", website=issue_to_add)
    st.success(f"Added {issue_to_add} to bookmarks.")

st.divider()

st.header("Saved Issues:")
for i, issue in enumerate(st.session_state.bookmarked_issues):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(issue)
    with col2:
        if st.button("🗑️ Delete", key=f"delete_{i}"):
            st.session_state.bookmarked_issues.pop(i)
            delete_bookmark_from_db(type="issue", website=issue)
            st.rerun()

