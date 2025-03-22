from crewai import Agent, Crew, Process, Task
from tools.custom_tools import jira_tool, get_qdrant_tool

# -- Jira Issues Agent --
jira_agent = Agent(
    role="Jira Issues Agent",
    goal="Find and fetch Jira issues using JQL Queries based on on the project in '{query}'",
    backstory="""You are a JQL expert who can generate accurate JQL queries and fetch the relevant Jira issues using the project in {query}.""",
    verbose=True,
    tools=[jira_tool]
)

jira_task = Task(
    description="""Find and fetch Jira issues using JQL Queries based on on the project in {query}.
    Your final answer should include:
    - The relevant Jira issues found""",
    agent=jira_agent,
    expected_output="A bullet list summary of the top 5 issues based on the project in {query}",
    verbose=True
)

# -- Semantic Search Agent --
semantic_search_agent = Agent(
    role="Senior Semantic Search Agent",
    goal="Find and analyze documents based on semantic search",
    backstory="""You are an expert research assistant who can find relevant information using semantic search in a Qdrant database.""",
    tools=[get_qdrant_tool("RESOURCE_MANAGEMENT")],
    verbose=True
)

semantic_search_task = Task(
    description="""Search for relevant documents about the {query}.
    Your final answer should include:
    - The relevant information found
    - The similarity scores of the results
    - The metadata of the relevant documents""",
    agent=semantic_search_agent,
    verbose=True
)

# -- Internal Risk Analysis Agent --
internal_risk_analysis_agent = Agent(
    role="Internal Risk Analysis Expert",
    goal="Generate answers to '{query}' based on the context provided",
    backstory="""You are a risk analysis expert who can analyze context comprising of Project Resources' Data and the metadata of relevant documents, the project issues retreived from Jira, analyze the internal risks in the project and generate answers to '{query}'.""",
    verbose=True
)

internal_risk_analysis_task = Task(
    description="""Analyze the context provided and generate answers to '{query}'.
    Your final answer should include:
    - The internal risks in the project""",
    agent=internal_risk_analysis_agent,
    context=[jira_task, semantic_search_task],
    verbose=True
)

def return_project_status_tracking_crew() -> Crew:
    return Crew(
        agents=[jira_agent, semantic_search_agent, internal_risk_analysis_agent],
        tasks=[jira_task, semantic_search_task, internal_risk_analysis_task],
        process=Process.sequential,
        output_log_file="crews/logs/project_status_tracking_crew.txt",
        verbose=True
    )