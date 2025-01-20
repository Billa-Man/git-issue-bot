import streamlit as st

from langchain_openai.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.schema import ChatMessage
from langchain.callbacks.base import BaseCallbackHandler

from settings import settings
from application.chat_tools import tools
from database.functions.sidebar_functions import get_chat_history, save_chat_history

#---------- TITLE ----------
st.set_page_config(page_title='Home')
st.header('Chat with the bot')

st.logo("application/git-issue-hound-logo.png", size='large')

#---------- CALLBACK HANDLER ----------
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token

#---------- SIDEBAR ----------
with st.sidebar:
    st.header("Chat History")
    
    chat_histories = get_chat_history()
    
    chat_labels = ["New Chat"]
    for chat in chat_histories:
        first_message = next((msg['content'] for msg in chat[0] if msg['role'] == 'user'), "Empty Chat")
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
                st.query_params['reload'] = 'true'
                st.rerun()
        with col2:
            if st.button("Load Chat", type="secondary", use_container_width=True):
                chat_index = chat_labels.index(selected_chat)
                loaded_messages = chat_histories[chat_index][0]
                st.session_state.messages = [
                    ChatMessage(
                        role=msg['role'],
                        content=msg['content']
                    ) for msg in loaded_messages
                ]
                st.query_params['reload'] = 'true'
                st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("New Chat", type="primary", use_container_width=True):
                st.session_state.messages = [ChatMessage(role="assistant", content="Hi, How can I help you?")]
                st.query_params['reload'] = 'true'
                st.rerun()


#---------- CHATBOT ---------
chat_tools = tools

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        return_messages=True,
        output_key="output", 
        human_prefix="user",
        ai_prefix="assistant",
        k=3
    )

if "agent_executor" not in st.session_state:
    stream_handler = StreamHandler(st.empty())
    llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, streaming=True, callbacks=[stream_handler])
    st.session_state.agent_executor = create_conversational_retrieval_agent(
        llm, 
        tools=chat_tools, 
        memory_key='chat_history', 
        verbose=True,
        system_message="You are a helpful assistant whose job is to interact with the user and answer their queries. If prompted, use the relevant tools to format your answers."
    )

#---------- CHAT OUTPUT ----------
if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="Hi, How can I help you?")]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not settings.OPENAI_API_KEY:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    assistant_message = st.chat_message("assistant")
    with assistant_message:
        stream_handler = StreamHandler(assistant_message)
        response = st.session_state.agent_executor.invoke({"input": prompt})
        st.session_state.messages.append(ChatMessage(role="assistant", content=response['output']))
        st.write(response['output'])
        save_chat_history()