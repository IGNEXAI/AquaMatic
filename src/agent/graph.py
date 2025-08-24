from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model


class AgentState(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

llm = init_chat_model("google_genai:gemini-2.5-flash")

# Define the nodes for the graph
def chatbot(state: AgentState):
    return {"messages": [llm.invoke(state["messages"])]}

# Define the graph
workflow = StateGraph(AgentState)
workflow.add_node("chatbot", chatbot)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

# Compile the graph
graph = workflow.compile()
