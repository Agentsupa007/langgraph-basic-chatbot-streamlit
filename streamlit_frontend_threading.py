import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage,AIMessage
import uuid

#********************utility functions**********************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    st.session_state["message_history"] = []
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )

    if "messages" in state.values:
        return state.values["messages"]
    else:
        return []

#***************************state management*********************************

# streamlit.session_state is a dictionary that can be used to store state across reruns of the app.
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

add_thread(st.session_state["thread_id"])

#************************sidebar ui*********************************

st.sidebar.title("LangGraph chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()


st.sidebar.header("My Conversations")

for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = "user"
            else:
               role = "assistant"

            temp_messages.append({"role": role, "content": msg.content})
        st.session_state["message_history"] = temp_messages
#***********************************main ui*********************************

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type your message here...")

CONFIG = {"configurable": {"thread_id":st.session_state["thread_id"]}}

if user_input:

    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)


    response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]},config=CONFIG)
    ai_message = response["messages"][-1].content

    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        st.text(ai_message)

    