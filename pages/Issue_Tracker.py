import streamlit as st
from langchain.schema import ChatMessage

from settings import settings
from github_tools import GitHubIssueSearchTool
from application.functions.display_outputs import display_issues
from database.functions.sidebar_functions import get_chat_history

#---------- TITLE ----------
st.set_page_config(page_title='Issue Tracker')
st.title('Issue Tracker')

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

if st.button("Search Issues", type="primary"):
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