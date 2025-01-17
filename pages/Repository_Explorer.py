import streamlit as st

from github_tools import GitHubRepoExplorerTool
from settings import settings
from application.functions import display_repos

st.title('Repository Explorer')

#---------- Main Filters ----------
col1, col2 = st.columns(2)
with col1:
    language = st.text_input("Programming Language")
    topic = st.text_input("Topic")

with col2:
    labels = st.text_input("Labels (comma-separated)")
    sort_by = st.selectbox(
        "Sort By",
        ["stars", "forks", "watchers", "created", "updated", "pushed"]
    )

limit = st.slider("Number of Results", min_value=1, max_value=100, value=10)


#---------- Advanced Filters ----------

with st.expander("Advanced Filters", expanded=True):

    query = st.text_input("Search Query")

    st.subheader("Numeric Filters")

    col3, col4, col5 = st.columns(3)
    with col3:
        min_stars = st.number_input("Min Stars", min_value=0)
        max_stars = st.number_input("Max Stars", min_value=0)

    with col4:
        min_forks = st.number_input("Min Forks", min_value=0)
        max_forks = st.number_input("Max Forks", min_value=0)

    with col5:
        min_issues = st.number_input("Min Issues", min_value=0)
        max_issues = st.number_input("Max Issues", min_value=0)

    st.subheader("Date Filters")

    col6, col7 = st.columns(2)
    with col6:
        created_after = st.date_input("Created After")
        updated_after = st.date_input("Updated After")
        pushed_after = st.date_input("Pushed After")

    with col7:
        created_before = st.date_input("Created Before")
        updated_before = st.date_input("Updated Before")
        pushed_before = st.date_input("Pushed Before")

#---------- Search Repositories ----------
if st.button("Apply Filters"):
    tool_input = {
        "language": language,
        "topic": topic,
        "labels": [label.strip() for label in labels.split(",") if label.strip()],
        "sort_by": sort_by,
        "limit": limit,
        "min_stars": min_stars if created_before else None,
        "max_stars": max_stars if created_before else None,
        "min_forks": min_forks if created_before else None,
        "max_forks": max_forks if created_before else None,
        "min_issues": min_issues if created_before else None,
        "max_issues": max_issues if created_before else None,
        "query": query if created_before else None,
        "created_before": created_before.isoformat() if created_before else None,
        "created_after": created_after.isoformat() if created_after else None,
        "updated_before": updated_before.isoformat() if updated_before else None,
        "updated_after": updated_after.isoformat() if updated_after else None,
        "pushed_before": pushed_before.isoformat() if pushed_before else None,
        "pushed_after": pushed_after.isoformat() if pushed_after else None
    }

    github_repo_tool = GitHubRepoExplorerTool(github_token=settings.GITHUB_API_TOKEN)

    with st.spinner("Searching repositories..."):
        repos = github_repo_tool.invoke(tool_input)

    if isinstance(repos, list):
        display_repos(repos, num_issues=tool_input['limit'])
    else:
        st.warning("No repositories found matching the specified criteria.")


#---------- Sidebar ----------
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