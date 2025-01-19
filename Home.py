import streamlit as st

from langchain_openai.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.schema import ChatMessage
from langchain.callbacks.base import BaseCallbackHandler

from settings import settings
from application.chat_tools import tools
from application.functions import get_button_label

#---------- TITLE ----------
st.set_page_config(page_title='Home')
st.title('Git Issue Hound')

st.logo("application/git-issue-hound-logo.png", size='large')

#---------- CALLBACK HANDLER ----------
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text, unsafe_allow_html=True)

#---------- CHATBOT ---------
chat_tools = tools

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True,
        output_key="output"
    )

if "agent_executor" not in st.session_state:
    stream_handler = StreamHandler(st.empty())
    llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, streaming=True, callbacks=[stream_handler])
    st.session_state.agent_executor = create_conversational_retrieval_agent(
        llm, 
        tools=chat_tools, 
        memory_key='chat_history', 
        verbose=True
    )

#---------- CHAT OUTPUT ----------
if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]

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

#---------- SIDEBAR ----------
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("Chat History")
    for chat_id, chat in enumerate(st.session_state.chat_history):
        button_label = get_button_label(chat_id, chat["first_message"])
        if st.button(button_label):
            st.session_state.current_chat = chat["messages"]