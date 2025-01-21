import streamlit as st
from database.functions.bookmark_functions import add_bookmark_to_db, get_bookmarks_from_db

#---------- DISPLAY RESULTS ----------
@st.fragment
def display_issues(results, num_issues=100):
    if 'bookmarked_issues' not in st.session_state:
        st.session_state.bookmarked_issues = get_bookmarks_from_db(type="issue")

    for result in results[:num_issues]:
        with st.container():
            issue_key = f"bookmark_{result['url']}"
            col1, col2, col3 = st.columns([0.8, 0.1, 0.1])

            with col1:
                st.markdown(f"### {result['title']}")
            with col2:
                st.link_button(label="👁️", url=result['url'], type="primary", use_container_width=True)
            with col3:
                is_bookmarked = result['url'] in st.session_state.bookmarked_issues

                if st.button(
                    label="✅" if is_bookmarked else "➕",
                    key=issue_key,
                    type="primary",
                    disabled=is_bookmarked,
                    use_container_width=True
                ):
                    if not is_bookmarked:
                        add_bookmark_to_db(type="issue", website=result['url'])
                        st.session_state.bookmarked_issues.append(result['url'])
                        st.success("✅")

            st.markdown(f"{result['summary']}")
            st.divider()


@st.fragment
def display_repos(results, num_repos=100):
    if 'bookmarked_repos' not in st.session_state:
        st.session_state.bookmarked_repos = get_bookmarks_from_db(type="repository")

    for result in results[:num_repos]:
        with st.container():
            repo_key = f"bookmark_{result['url']}"
            col1, col2, col3 = st.columns([0.8, 0.1, 0.1])

            with col1:
                st.markdown(f"### {result['name']}")
            with col2:
                st.link_button(label="👁️", url=result['url'], type="primary", use_container_width=True)
            with col3:
                is_bookmarked = result['url'] in st.session_state.bookmarked_repos

                if st.button(
                    label="✅" if is_bookmarked else "➕",
                    key=repo_key,
                    type="primary",
                    disabled=is_bookmarked,
                    use_container_width=True
                ):
                    if not is_bookmarked:
                        add_bookmark_to_db(type="repository", website=result['url'])
                        st.session_state.bookmarked_repos.append(result['url'])
                        st.success("✅")

            st.markdown(f"{result['description']}")
            st.markdown(f"⭐: {result['stars']} | 🍴: {result['forks']} | 🚧: {result['open_issues']}")
            st.markdown(f"**Language**: {result['language']}")
            st.markdown(f"**Topics**: {', '.join(result['topics'])}")

            st.divider()