import streamlit as st
from github_tools import GitHubIssueSearchTool

from settings import settings
from application.functions import display_issues
from database.db_functions import get_chat_history

#---------- TITLE ----------
st.set_page_config(page_title='Issue Tracker')
st.title('Issue Tracker')

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

#---------- TOPICS ----------
languages = ["python", "javascript", "java", "cpp", "go"]
selected_language = st.selectbox("Select Language:", options =  languages + ["Others"])
if selected_language == "Others":
    selected_language = st.text_input("Enter the language:")

default_github_labels = ['bug', 'documentation', 'duplicate', 'enhancement', 'good first issue',
                         'help wanted', 'invalid', 'question', 'wontfix']


selected_labels = st.multiselect(
    "Select Label Categories",
    options = default_github_labels + ["Others"],
    placeholder="Choose categories"
)

if "Others" in selected_labels:
    selected_labels = selected_labels[:-1]
    other_labels = st.text_input("Enter the labels (separated by commas)")
    other_labels = [label.strip() for label in other_labels.split(",")  if label.strip()]
    selected_labels.extend(other_labels)

num_results = st.text_input("Enter number of results returned:")

if num_results:
    if num_results.isnumeric():
        num_results = int(num_results)
    else:
        st.error("Please enter a valid integer")

#---------- DISPLAY SELECTION ----------
st.write(f"Language: {selected_language} | Labels: {selected_labels} | Number of Results: {num_results}")

#---------- SEARCH BUTTON ----------
github_issue_tool = GitHubIssueSearchTool(github_token=settings.GITHUB_API_TOKEN)

if st.button("Search Repositories and Issues"):
    inputs = {
        "language": selected_language,
        "labels": selected_labels,
    }

    with st.spinner("Searching issues..."):
        issues = github_issue_tool.invoke(inputs)

    if isinstance(issues, list):
        display_issues(issues, num_issues=num_results)
    else:
        st.warning("No issues found matching the specified criteria.")