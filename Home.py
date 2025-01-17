import streamlit as st

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