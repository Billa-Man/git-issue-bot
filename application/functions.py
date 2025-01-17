import streamlit as st
import random

def display_issues(results, num_issues=10):

    random_results = random.sample(results, min(num_issues, len(results)))
    
    for result in random_results[:num_issues]:
        with st.container():

            st.markdown(f"### {result['title']}")
            st.markdown(f"{result['summary']}")
            st.markdown(f"##### [View Issue →]({result['url']})")
            
            st.divider()


def display_repos(results, num_issues=10):

    random_results = random.sample(results, min(num_issues, len(results)))
    
    for result in random_results[:num_issues]:
        with st.container():

            st.markdown(f"### {result['name']}")
            st.markdown(f"{result['description']}")
            st.markdown(f"##### Stars: {result['stars']} | Forks: {result['forks']} | Open Issues: {result['open_issues']}")
            st.markdown(f"##### Language: {result['language']} | Topics: {', '.join(result['topics'])}")
            st.markdown(f"##### Last Updated: {result['last_updated']}")
            st.markdown(f"##### [View Repository →]({result['url']})")

            st.divider()