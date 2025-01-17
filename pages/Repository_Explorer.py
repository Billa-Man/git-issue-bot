import streamlit as st

from github_tools import GitHubRepoExplorerTool
from settings import settings
from application.functions import display_repos, get_button_label

st.title('Repository Explorer')

#---------- Main Filters ----------
col1, col2 = st.columns(2)
with col1:
    languages = ["python", "javascript", "java", "cpp", "go"]
    language = st.selectbox("Select Language:", options =  languages + ["Others"])
    if language == "Others":
        language = st.text_input("Enter the language:")

    topics = st.text_input("Topic (separated by commas)")
    if topics:
        topics = [t.strip() for t in topics.split(",") if t.strip()]
    else:
        topics = []

with col2:
    labels = st.text_input("Labels (separated by commas)")
    if labels:
        labels = [label.strip() for label in labels.split(",") if label.strip()]
    else:
        labels = []

    sort_by = st.selectbox(
        "Sort By",
        ["stars", "forks", "watchers", "created", "updated", "pushed"]
    )

limit = st.slider("Number of Results", min_value=1, max_value=100, value=10)


#---------- Advanced Filters ----------

with st.expander("Advanced Filters", expanded=False):

    query = st.text_input("Search Query")

    st.subheader("Numeric Filters")

    col3, col4, col5 = st.columns(3)
    with col3:
        min_stars = st.number_input(label = "Min Stars", value = None, min_value=0)
        max_stars = st.number_input(label = "Max Stars", value = None, min_value=0)

    with col4:
        min_forks = st.number_input(label = "Min Forks", value = None, min_value=0)
        max_forks = st.number_input(label = "Max Forks", value = None, min_value=0)

    with col5:
        min_issues = st.number_input(label = "Min Issues", value = None, min_value=0)
        max_issues = st.number_input(label = "Max Issues", value = None, min_value=0)

    st.subheader("Date Filters")

    col6, col7 = st.columns(2)
    with col6:
        created_after = st.date_input(label = "Created After", value = None)
        updated_after = st.date_input(label = "Updated After", value = None)
        pushed_after = st.date_input(label = "Pushed After", value = None)

    with col7:
        created_before = st.date_input(label = "Created Before", value = None)
        updated_before = st.date_input(label = "Updated Before", value = None)
        pushed_before = st.date_input(label = "Pushed Before", value = None)

#---------- Search Repositories ----------
if st.button("Apply Filters"):
    tool_input = {
        "language": language,
        "topics": topics,
        "labels": labels,
        "sort_by": sort_by,
        "limit": limit,
        "min_stars": min_stars if min_stars else None,
        "max_stars": max_stars if max_stars else None,
        "min_forks": min_forks if min_forks else None,
        "max_forks": max_forks if max_forks else None,
        "min_issues": min_issues if min_issues else None,
        "max_issues": max_issues if max_issues else None,
        "query": query if query else None,
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

with st.sidebar:
    st.header("Chat History")
    for chat_id, chat in enumerate(st.session_state.chat_history):
        button_label = get_button_label(chat_id, chat["first_message"])
        if st.button(button_label):
            st.session_state.current_chat = chat["messages"]