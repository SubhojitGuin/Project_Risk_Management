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
class TransactionRiskAnalysisCrew:
    @agent
    def agent(self) -> Agent:
        return Agent(
            role="""Transaction Risk Analysis Agent specialized in identifying and analyzing potential risks associated with financial transactions.""",
            goal="""Your goal is to provide the potential risks and insights based on the transaction data provided in {transaction_records} using the rules specified in {static_records}. You will also consider external factors from {market_records} to enhance your analysis. Your goal is to ensure that the transaction data is thoroughly analyzed for any potential risks, and you will provide a detailed report on your findings.""",
            backstory="""
            You are a Transaction Risk Analysis Agent with 10+ years of expertise in identifying and analyzing potential risks associated with financial transactions using the rules specified in {static_records}. You have a deep understanding of transaction patterns, market dynamics, and regulatory requirements. Your role is to analyze transaction data and identify any potential risks that may arise from them. You will leverage your knowledge of external factors and static rules to provide a comprehensive risk analysis.
            """,
            llm=llm,
            verbose=True,
        )

    @task
    def task(self) -> Task:
        return Task(
            name="Transaction Risk Analysis",
            description="""
            Analyze the transactions in {transaction_records} in conjunction with pre-defined risk evaluation criteria {static_records} and dynamic market indicators {market_records}. Identify and categorize risks such as financial anomalies, compliance breaches, budget overruns, suspicious vendor behavior, and potential fraud. Generate a structured and detailed report that outlines key risk areas, their severity, root causes, and suggested mitigation steps.
            """,
            expected_output="""
            A txt file containing a detailed report on the transaction risk analysis including the following sections, also include mitigation steps for each risk identified:

            - Integrity & Anomalies: Duplicate Transactions, Outlier Detection, Invoice Mismatches
            - Compliance: Policy Violations, Manual Overrides, Approval Process Bypasses
            - Fraud Risk: Multiple Payments to Same Vendor/Account, Unusual Fund Flows, Unjustified Transactions
            - Vendor Risk: Vendor Performance Issues, Compliance Flags, High Dependency Vendors
            - Financial Exposure: Budget Variance, Overdue Payments, Credit Exposure, Spend over Authorization
            - Operational Risk: Timeline Impact, Resource Risk, High Cloud Spend
            - Audit & Traceability: Audit Trail Completeness, Last Audit Findings, Mitigation Actions Taken
            - Quantitative Score: Risk Rating (Low/Med/High), Transaction Risk Score (0–100)
            - Categorization: Transaction Type, Department/Cost Center, Risk Category (Compliance/Fraud/etc.)

            Do not include the markdown symbols in the output. The report should be structured and easy to read, with clear headings and subheadings for each section. Use bullet points or numbered lists where appropriate to enhance readability.
            """,
            output_file="output/transaction_risk_analysis.txt",
            agent=self.agent(),
            verbose=True
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            name="Transaction Risk Analysis Crew",
            description="A crew specialized in analyzing transaction data for risk assessment.",
            agents=[self.agent()],
            tasks=[self.task()],
            process = Process.sequential,
            verbose=True
        )
    
if __name__ == "__main__":
    with open("project_details/resource.json", "r") as f:
        transaction_records = json.load(f)
    with open("project_details/static_rules.json", "r") as f:
        static_records = json.load(f)
        static_records = static_records["transaction_rules"]
    with open("project_details/market_analysis_summary.json", "r") as f:
        market_records = json.load(f)
    TransactionRiskAnalysisCrew().crew().kickoff({"transaction_records": transaction_records, "static_records": static_records, "market_records": market_records})
