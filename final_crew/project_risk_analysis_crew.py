from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew
import os
from dotenv import load_dotenv
import json
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


llm = LLM(
    model=os.getenv("MODEL"),
    temperature=0.5,
    base_url="https://api.openai.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

    
@CrewBase
class ProjectRiskAnalysisCrew:
    @agent
    def agent(self) -> Agent:
        return Agent(
           role = """
            Project Risk Analysis Agent specializing in identifying, evaluating, and forecasting risks across project lifecycle dimensions including delivery, budget, quality, compliance, stakeholder engagement, and technical integration.
            """,
            goal="""Your goal is to provide the potential risks and insights based on the project data provided in {project_records} using the rules specified in {static_records}.Your goal is to provide strategic insights, risk scores, and prioritized recommendations that enable timely decision-making and safeguard project objectives, and you will provide a detailed report on your findings.""",
            backstory = """
            You are a Project Risk Analysis Agent with 10+ years of experience in advanced risk modeling and multi-dimensional project assessments. You specialize in interpreting structured rules from {static_records} to identify hidden patterns, anomalies, and early warnings in {project_records}. Your expertise spans key risk domains such as delivery delays, milestone slippage, velocity drops, backlog growth, cost overruns, stakeholder conflicts, security gaps, and governance lapses.
            """,
            llm=llm,
            verbose=True,
        )
            
    @task
    def task(self) -> Task:
        return Task(
            name="Resource Risk Analysis",
            description="""
            Analyze the project's current phase data {project_records} and correlate it with {static_records} to detect risk conditions across the following 17 risk categories:

            Delivery, Velocity, Backlog, Budget, Quality, Issues, Change Management, Strategic Alignment, Governance, Reporting, Security Compliance, Technical Integration, Risk Process, Stakeholder, Release, Agility, and Overall Risk Score.
            """,
            expected_output="""
            A txt file containing a detailed report on the project risk analysis including the following sections:
            
            - Classify each risk category into one of the levels: Low, Medium, High, or Critical.
            - Highlight breached thresholds or anomalies triggering the risk.
            - Provide a reason or analysis for each flagged risk.
            - Suggest actionable mitigation recommendation for each flagged risk.
            - Generate a final Overall Risk Score (0–100) and corresponding Risk Level.

            The txt file should NOT include the markdown symbols in the output (like **, #, ---). The report should be structured and easy to read, with clear headings and subheadings for each section. Use bullet points or numbered lists where appropriate to enhance readability.
            """,
            output_file="output/project_risk_analysis.txt",
            agent=self.agent(),
            verbose=True
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            name="Project Risk Analysis Crew",
            description="A crew specialized in analyzing project details for risk assessment.",
            agents=[self.agent()],
            tasks=[self.task()],
            process = Process.sequential,
            verbose=True
        )
    
if __name__ == "__main__":
    with open("project_details/project.json", "r") as f:
        project_records = json.load(f)
    with open("project_details/static_rules.json", "r") as f:
        static_records = json.load(f)
        static_records = static_records["project_risk_rules"]
    ProjectRiskAnalysisCrew().crew().kickoff({"project_records": project_records, "static_records": static_records})
