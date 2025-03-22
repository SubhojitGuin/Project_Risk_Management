from crewai import Agent, Crew, Process, Task

mitigation_strategies_agent = Agent(
    role="Mitigation Strategies Agent",
    goal= """Generate mitigation strategies for the risks identified in the project based on the data provided.
    Risks in the Project:
    {risks}
    """,
    backstory="""You are a mitigation strategies expert, with 10 years of experience in Project Management, who can generate mitigation strategies for the risks identified in the project based on the data provided.""",
    verbose= True
)

mitigation_strategies_task = Task(
    description="""Generate mitigation strategies for the risks identified in the project based on the data provided.
    Your final answer should include:
    - The mitigation strategies for the risks identified in the project.

    Risks in the Project:
    {risks}
    """,
    agent=mitigation_strategies_agent,
    expected_output="""
    - The mitigation strategies for the risks identified in the project.
    """,
    verbose=True
)

def mitigation_strategies_crew() -> Crew:
    return Crew(
        agents=[mitigation_strategies_agent],
        tasks=[mitigation_strategies_task],
        process=Process.sequential,
        output_log_file="crews/logs/mitigation_strategies_crew.txt",
        verbose=True
    )
