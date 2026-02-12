from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict,Literal,Annotated
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):

    messages = state["messages"]

    response = llm.invoke(messages)
    
    return {"messages": [response]}

graph = StateGraph(ChatState)

checkpointer = InMemorySaver()

graph.add_node("chat",chat_node)

graph.add_edge(START,"chat")
graph.add_edge("chat",END) 

chatbot = graph.compile(checkpointer=checkpointer)