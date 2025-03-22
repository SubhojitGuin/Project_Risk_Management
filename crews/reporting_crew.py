from crewai import Agent, Crew, Process, Task

reporting_agent = Agent(
    role="",
    goal="",
    backstory="",
    verbose=True
)

reporting_task = 