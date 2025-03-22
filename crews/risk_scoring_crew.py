from crewai import Agent, Crew, Process, Task


risk_scoring_agent = Agent(
    role="Risk Scoring Agent",
    goal="""Calculate the risk score and classify them into one the four categories ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW') based on the data provided.
    Investment Risks in the Project:
    {investment_risks}

    Internal Risks in the Project:
    {internal_risks}
    """,
    backstory="""You are a risk scoring expert, with 10 years of experience in Project Management, who can calculate the risk score and classify them into one the four categories ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW') based on the data provided.""",
    verbose=True
)

risk_scoring_task = Task(
    description="""Calculate the risk score based on the data (Investment Risks, Internal Risks) provided.
    Your final answer should include:
    - The risks along with their risk scores classisfied into one of the four categories ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')
    - The explanation of the risk score calculated for each risk.

    Investment Risks in the Project:
    {investment_risks}
    Internal Risks in the Project:
    {internal_risks}
    """,
    agent=risk_scoring_agent,
    expected_output=""""
    - The risks along with their risk scores classisfied into one of the four categories ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')
    - The explanation of the risk score calculated for each risk.
    """,
    verbose=True
)

def return_risk_scoring_crew() -> Crew:
    return Crew(
        agents=[risk_scoring_agent],
        tasks=[risk_scoring_task],
        process=Process.sequential,
        output_log_file="crews/logs/risk_scoring_crew.txt",
        verbose=True
    )

