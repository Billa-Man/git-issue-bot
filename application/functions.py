import streamlit as st
import random
import json

from database.db_functions import add_bookmark_to_db

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

            col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
            with col1:
                st.markdown(f"### {result['title']}")
            with col2:
                st.link_button(label = " 👁️ View", url = result['url'], use_container_width=True)
            with col3:
                is_saved = result['url'] in st.session_state.saved_issues
                if is_saved:
                    st.success("Issue already saved in bookmarks", unsafe_allow_html=True)
                else:
                    if st.button("🔖 Save", key=f"bookmark_{result['name']}", use_container_width=True):
                        try:
                            add_bookmark_to_db(type="issue", website=result['url'])
                            st.session_state.saved_issues.add(result['url'])
                            st.success("✅ Saved Issue!")
                        except Exception as e:
                            st.error("Failed to save")

            st.markdown(f"{result['summary']}")
            
            st.divider()


def display_repos(results, num_issues=10):

    random_results = random.sample(results, min(num_issues, len(results)))
    
    for result in random_results[:num_issues]:
        with st.container():

            col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
            with col1:
                st.markdown(f"### {result['name']}")
            with col2:
                st.link_button(label = " 👁️ View", url = result['url'], use_container_width=True)
            with col3:
                is_saved = result['url'] in st.session_state.saved_repos
                if is_saved:
                    st.success("Repository already saved in bookamarks", unsafe_allow_html=True)
                else:
                    if st.button("🔖 Save", key=f"bookmark_{result['name']}", use_container_width=True):
                        try:
                            add_bookmark_to_db(type="repository", website=result['url'])
                            st.session_state.saved_repos.add(result['url'])
                            st.success("✅ Saved Repository!")
                        except Exception as e:
                            st.error("Failed to save")

            st.markdown(f"{result['description']}")
            st.markdown(f"⭐: {result['stars']} | **Forks**: {result['forks']} | **Open Issues**: {result['open_issues']}")
            st.markdown(f"**Language**: {result['language']}")
            st.markdown(f"**Topics**: {', '.join(result['topics'])}")
            
            st.divider()


def get_button_label(chat_id, first_message):
    return f"Chat {chat_id}: {' '.join(first_message.split()[:5])}..."