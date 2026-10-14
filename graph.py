
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from agents import topics, summary, actions, priority

class State(TypedDict, total=False):
    transcript: str
    topics: str
    summary: str
    actions: str
    priority: str
    report: str

def input_node(state):
    if not state["transcript"].strip():
        raise ValueError("Please enter a meeting transcript.")
    return {}

def check_actions(state):
    if "NO ACTION ITEMS" in state["actions"].upper():
        return "report"
    return "priority"

def report(state):
    no_actions = "NO ACTION ITEMS" in state["actions"].upper()

    return {
        "report": f"""
## Meeting Summary
{state['summary']}

## Key Topics
{state['topics']}

## Action Items
{state['actions']}

## Task Owners
{"No task owners identified." if no_actions else state['actions']}

## Priority Level
{"No action items identified in this meeting." if no_actions else state['priority']}
"""
    }

graph = StateGraph(State)

graph.add_node("input", input_node)
graph.add_node("topics", topics)
graph.add_node("summary", summary)
graph.add_node("actions", actions)
graph.add_node("priority", priority)
graph.add_node("report", report)

graph.add_edge(START, "input")
graph.add_edge("input", "topics")
graph.add_edge("topics", "summary")
graph.add_edge("summary", "actions")

graph.add_conditional_edges(
    "actions",
    check_actions,
    {
        "priority": "priority",
        "report": "report"
    }
)

graph.add_edge("priority", "report")
graph.add_edge("report", END)

app = graph.compile()