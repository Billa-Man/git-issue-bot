import streamlit as st
import random
import json

#---------- CHATBOT OUTPUT ----------
def store_message(messages, role, content):
    if not isinstance(content, str):
        content = json.dumps(content)
    messages.append({"role": role, "content": content})


def detect_output_type(response):
    if isinstance(response, str):
        return "string"
    elif isinstance(response, dict):
        return "dictionary"
    elif isinstance(response, list):
        return "list"
    else:
        return "unknown"


def process_chatbot_output(output):
    output_type = detect_output_type(output)
    
    if output_type == "string":
        st.write(output)
    elif output_type in ["dictionary", "list"]:
        st.json(output)
    else:
        st.error("Unknown response type received.")

#---------- MANUAL MODE ----------
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
            st.markdown(f"⭐: {result['stars']} | **Forks**: {result['forks']} | **Open Issues**: {result['open_issues']}")
            st.markdown(f"**Language**: {result['language']}")
            st.markdown(f"**Topics**: {', '.join(result['topics'])}")
            st.markdown(f"##### [View Repository →]({result['url']})")
            
            st.divider()