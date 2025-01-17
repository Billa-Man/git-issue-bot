import streamlit as st
import random

def display_issues(results, num_issues=10):

    random_results = random.sample(results, min(num_issues, len(results)))
    
    for result in random_results[:num_issues]:
        with st.container():

            st.markdown(f"#### {result['title']}")
            st.markdown(f"{result['summary']}")
            st.markdown(f"##### [View Issue →]({result['url']})")
            
            # Add a visual separator
            st.divider()