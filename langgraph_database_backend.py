from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict,Literal,Annotated
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver

import sqlite3

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):

    messages = state["messages"]

    response = llm.invoke(messages)
    
    return {"messages": [response]}


conn = sqlite3.connect("chatbot.db",check_same_thread=False)

graph = StateGraph(ChatState)

checkpointer = SqliteSaver(conn=conn)

graph.add_node("chat",chat_node)

graph.add_edge(START,"chat")
graph.add_edge("chat",END) 

chatbot = graph.compile(checkpointer=checkpointer)


def reterieve_all_threads():
    all_threads = set()

    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])

    return (list(all_threads))