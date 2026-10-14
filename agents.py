
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def topics(state):
    prompt = f"List the main topics of this meeting:\n{state['transcript']}"
    result = llm.invoke(prompt)
    return {"topics": result.content}

def summary(state):
    prompt = f"Summarize this meeting in 3 to 5 sentences:\n{state['transcript']}"
    result = llm.invoke(prompt)
    return {"summary": result.content}

def actions(state):
    prompt = f"""
Find all action items from this meeting.
Include the task and its owner.
If the owner is unknown, write Owner: Not specified.
If there are no action items, write exactly NO ACTION ITEMS.

Meeting:
{state['transcript']}
"""
    result = llm.invoke(prompt)
    return {"actions": result.content}

def priority(state):
    prompt = f"""
Choose one priority level: High Priority, Medium Priority, or Low Priority.

High: urgent, ASAP, critical, or due tomorrow.
Medium: important tasks due this week.
Low: tasks with no clear urgency.

Meeting:
{state['transcript']}

Action items:
{state['actions']}

Return only the priority level.
"""
    result = llm.invoke(prompt)
    return {"priority": result.content.strip()}