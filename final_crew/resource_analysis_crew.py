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
class ResourceRiskAnalysisCrew:
    @agent
    def agent(self) -> Agent:
        return Agent(
            role="""Resource Risk Analysis Agent specialized in identifying and analyzing potential risks associated with project resources management.""",
            goal="""Your goal is to provide the potential risks and insights based on the resources data provided in {resource_records} using the rules specified in {static_records}. You will also consider external factors from {market_records} to enhance your analysis. Your goal is to ensure that the resource data is thoroughly analyzed for any potential risks, and you will provide a detailed report on your findings.""",
            backstory="""
            You are a Resource Risk Analysis Agent with 10+ years of expertise in identifying and analyzing potential risks associated with project resources management using the rules specified in {static_records}. You operate with a nuanced understanding of various resource domains — including human, hardware, software, cloud, and storage facilities — evaluating everything from workforce availability and skill shortages to resource bottlenecks and compliance issues. You forecast potential threats by correlating {static_records} with real-time external factors from {market_records}.
            """,
            llm=llm,
            verbose=True,
        )
            
    @task
    def task(self) -> Task:
        return Task(
            name="Resource Risk Analysis",
            description="""
            You operate under the rules and standards defined in {static_records}, which outline thresholds, acceptable utilization levels, compliance requirements, and mitigation protocols for various types of resources and you must also consider external influences such as market dynamics, labor trends, regulatory changes, supply chain disruptions, and technology shifts from {market_records} and evaluate how they might amplify internal resource risks based on the resource data provided in {resource_records} and identify potential risks, including but not limited to:

            - Resource utilization (overuse, underuse, bottlenecks)
            - Forecasted shortages or surpluses
            - SLA compliance risks
            - Single points of failure or over-dependence on specific vendors, tools, personnel or services
            - Regulatory and operational compliance
            - Impact on project milestones and deliverables
            """,
            expected_output="""
            A txt file containing a detailed report on the resource risk analysis including the following sections, also include mitigation steps for each risk identified:

            - Overall risk level (Low / Medium / High / Critical) and Overall risk score (0-100)
            - Category-wise risk assessments
            - Identified issues and potential impacts
            - Rule-based justification (linked to {static_records})
            - Mitigation recommendations (both immediate and strategic)

            Do not include the markdown symbols in the output (like **, #). The report should be structured and easy to read, with clear headings and subheadings for each section. Use bullet points or numbered lists where appropriate to enhance readability.
           
            """,
            output_file="output/resource_risk_analysis.txt",
            agent=self.agent(),
            verbose=True
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            name="Resource Risk Analysis Crew",
            description="A crew specialized in analyzing project resources data for risk assessment.",
            agents=[self.agent()],
            tasks=[self.task()],
            process = Process.sequential,
            verbose=True
        )
    
if __name__ == "__main__":
    with open("project_details/resource.json", "r") as f:
        resource_records = json.load(f)
    with open("project_details/static_rules.json", "r") as f:
        static_records = json.load(f)
        static_records = static_records["resource_management_rules"]
    with open("project_details/market_analysis_summary.json", "r") as f:
        market_records = json.load(f)
    ResourceRiskAnalysisCrew().crew().kickoff({"resource_records": resource_records, "static_records": static_records, "market_records": market_records})
