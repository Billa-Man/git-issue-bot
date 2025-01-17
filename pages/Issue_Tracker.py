import streamlit as st

from github_tools import GitHubIssueSearchTool
from settings import settings

from application.functions import display_issues, get_button_label
from application.exceptions import NoIssuesFoundError

# Title
st.set_page_config(page_title='Issue Tracker')
st.title('Issue Tracker')

#---------- Topics ----------
languages = ["python", "javascript", "java", "cpp", "go"]
selected_language = st.selectbox("Select Language:", options =  languages + ["Others"])
if selected_language == "Others":
    selected_language = st.text_input("Enter the language:")

# Issue Tags
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

#---------- Display the selection ----------
st.write(f"Language: {selected_language} | Labels: {selected_labels} | Number of Results: {num_results}")

#---------- Search Button ----------
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

#---------- Sidebar ----------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("Chat History")
    for chat_id, chat in enumerate(st.session_state.chat_history):
        button_label = get_button_label(chat_id, chat["first_message"])
        if st.button(button_label):
            st.session_state.current_chat = chat["messages"]