import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage,AIMessage

# streamlit.session_state is a dictionary that can be used to store state across reruns of the app.

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type your message here...")

CONFIG = {"configurable": {"thread_id":"thread_1"}}

if user_input:

    
    with st.chat_message("user"):
        st.text(user_input)

    st.session_state["message_history"].append({"role": "user", "content": user_input})


        #     message_chunk.content 
        # for message_chunk, metadata in chatbot.stream(...)
        # is a generator expression.

        # It means:

        # For every streamed chunk, take only its .content text.
        
    with st.chat_message("assistant"):
        response = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                 stream_mode="messages",          
                config=CONFIG
            )
        )

    st.session_state["message_history"].append({"role": "assistant", "content": response})
