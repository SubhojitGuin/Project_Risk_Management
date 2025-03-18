from crewai import Agent, Crew, Process, Task
from tools.custom_tools import jira_tool

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

def return_project_status_tracking_crew() -> Crew:
    return Crew(
        agents=[jira_agent],
        tasks=[jira_task],
        process=Process.sequential,
        output_log_file="crews/logs/project_status_tracking_crew.txt",
        verbose=True
    )