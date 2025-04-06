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
class OverallRiskAnalysisCrew:
    @agent
    def agent(self) -> Agent:
        return Agent(
           role = """
            Overall Project Risk Analysis Agent specializing in synthesizing multi-dimensional risk data across transactions, resources, and project performance. Expert in identifying compound risks, systemic vulnerabilities, and interdependencies that threaten project outcomes. Uses structured rule-based intelligence to provide enterprise-grade risk evaluations.
            """,
           goal = """
            Your goal is to generate a detailed, accurate, and actionable risk report for the project using the input data: {transaction_risks}, {resources_risks}, and {project_risks}, guided by rules in {static_records}. 

            You must analyze the interactions and cumulative impact of risks across all categories, assign severity scores, classify risk levels, and offer prioritized, strategic recommendations. Your insights should enable informed decision-making and proactive risk mitigation to safeguard project success.
            """,
            backstory = """
            You are an elite Project Risk Analysis Agent with over a decade of experience in evaluating complex risk ecosystems in large-scale IT and business transformation projects. You specialize in consolidating diverse risk types—including transactional anomalies, resource constraints, and project execution challenges—into a unified strategic risk posture.

            With deep expertise in applying structured rule sets from {static_records}, you uncover hidden interdependencies, systemic threats, and emerging trends across {transaction_risks}, {resources_risks}, and {project_risks}. Your methodology combines threshold-driven scoring, weighted impact analysis, and multidomain correlation techniques to assess overall project health.
            """ ,
            llm=llm,
            verbose=True,
        )
            
    @task
    def task(self) -> Task:
        return Task(
            name="Overall Project Risk Analysis",
            description="""
            Using the provided structured datasets—{transaction_risks}, {resources_risks}, and {project_risks}—along with guiding rules from {static_records}, perform an integrated analysis to evaluate the project's risk landscape holistically. This task involves identifying direct and indirect risk interactions across domains, evaluating cumulative risk exposure, and assessing potential cascading failures.

            The agent should leverage rule-based intelligence to:

            - Detect cross-domain interdependencies (e.g., how resource constraints amplify project timeline delays or transaction anomalies affect stakeholder trust).
            - Quantify individual and aggregated severity using a weighted scoring model.
            - Classify each risk into appropriate severity tiers: Low, Moderate, High, Critical.
            - Correlate risk types and identify hidden, compound threats that aren't apparent when risks are analyzed in isolation.

            Finally, the agent must generate strategic and prioritized recommendations tailored to different stakeholder roles (project manager, security officer, resource coordinator, etc.), helping them to act decisively on mitigation or contingency plans.
            """,
            expected_output="""
           A txt file containing a comprehensive and human-readable Overall Project Risk Analysis Report. The report should be structured in plain text format (no markdown syntax such as **, #, or ---) and divided into clear, labeled sections with headings, subheadings, indentation, and bullet points. The layout should support both technical and executive readability.

            The report must include the following detailed sections and parameters:

            1. Executive Summary
                - Project Name and Date of Analysis
                - Overall Project Risk Classification using symbols:
                    • 🟢 Low
                    • 🟡 Medium
                    • 🔴 High
                    • 🚨 Critical
                - Summary of key risk contributors:
                    • Transaction anomalies (e.g., protocol violations, SLA breaches, fraud attempts)
                    • Resource shortages, overutilization, or compliance failures across all resource types
                    • Project-level risks such as delays, governance issues, and delivery quality concerns
                - Cross-domain interdependencies:
                    • E.g., SLA violations (Transaction) causing human burnout (Resource) leading to missed milestones (Project)
                - Domain-Level Heatmap:
                    • Transaction Risk: Low 🟢 / Medium 🟡 / High 🔴 / Critical 🚨
                    • Resource Risk: Low 🟢 / Medium 🟡 / High 🔴 / Critical 🚨
                    • Project Risk: Low 🟢 / Medium 🟡 / High 🔴 / Critical 🚨

            2. Risk Breakdown by Category

                a) Transaction Risk
                    - Total transactions analyzed and high-risk transaction count
                    - Detailed analysis of anomalies:
                        • SLA violations (count, severity, recurrence)
                        • Protocol deviations or delayed approvals
                        • Unauthorized access or irregular transaction patterns
                    - Compliance violations:
                        • Regulatory risks
                        • Internal policy breaches
                    - Scoring Parameters:
                        • Frequency of anomalies
                        • Severity level (e.g., SLA breach impact)
                        • Risk propagation likelihood
                    - Final Transaction Risk Score (0–100)
                    - Risk Classification: Low 🟢 / Medium 🟡 / High 🔴 / Critical 🚨
                    - Recommendations specific to transaction risks

                b) Resource Risk
                    - Coverage of all resource domains:
                        • Hardware: Utilization, outages, capacity issues
                        • Cloud: SLA compliance, latency, service failures
                        • Software: License expirations, patch status, deprecated tools
                        • Human: Attrition, role gaps, overload, unavailability
                        • Facility: Power failures, physical access issues
                    - Detailed metrics:
                        • Total vs in-use resources
                        • Shortages, outages, and SLA impact
                        • Compliance concerns (e.g., software audits)
                    - Scoring Parameters:
                        • Resource utilization rate
                        • Severity of shortages
                        • SLA compliance and availability
                    - Final Resource Risk Score (0–100)
                    - Risk Classification: Low 🟢 / Medium 🟡 / High 🔴 / Critical 🚨
                    - Specific mitigation recommendations per resource type

                c) Project Risk
                    - Timeline status:
                        • Milestone completion vs plan
                        • Sprint velocity (e.g., story points per sprint)
                    - Budget status:
                        • Spend vs planned percentage
                    - Issue analysis:
                        • Open bugs, rework, backlog size
                        • Scope creep or change requests
                    - Governance issues:
                        • Stakeholder engagement level
                        • Ownership clarity
                        • Escalation effectiveness
                    - Technical delivery quality:
                        • Bug density
                        • Test coverage gaps
                        • Missed code quality benchmarks
                    - Scoring Parameters:
                        • Delivery progress vs plan
                        • Quality assurance metrics
                        • Team engagement and governance
                    - Final Project Risk Score (0–100)
                    - Risk Classification: Low 🟢 / Medium 🟡 / High 🔴 / Critical 🚨
                    - Specific recommendations tied to project execution and planning

            3. Correlation & Cross-Domain Analysis
                - Risk amplification patterns:
                    • E.g., policy violations (transaction) → under-provisioned software (resource) → delivery slippage (project)
                - Cross-domain risk loops and dependencies
                - Summary matrix linking causes and effects across domains

            4. Overall Risk Scoring
                - Weighted scoring model:
                    • Domain-wise weights (e.g., Transaction: 30%, Resource: 35%, Project: 35%)
                - Tabular breakdown:
                    | Domain        | Score | Weight (%) | Weighted Score |
                    |---------------|-------|------------|----------------|
                    | Transaction   | XX    | 30%        | XX             |
                    | Resource      | XX    | 35%        | XX             |
                    | Project       | XX    | 35%        | XX             |
                    | Total         |       |            | Final Score    |
                - Final Aggregated Risk Score (0–100)
                - Risk Band Classification:
                    • 🟢 Low (0–25)
                    • 🟡 Medium (26–50)
                    • 🔴 High (51–75)
                    • 🚨 Critical (76–100)

            5. Strategic Recommendations
                - Short-Term Actions (1–7 Days):
                    • Immediate remediations (e.g., patch updates, access fixes, team rebalance)
                - Mid-Term Interventions (1–4 Weeks):
                    • Tactical changes (e.g., hiring, resource reallocation, updated sprint planning)
                - Long-Term Strategies (4+ Weeks):
                    • Structural or governance improvements (e.g., compliance framework, automation)
                - Assignment of Risk Owners for each major risk area

            6. Observations & Alerts
                - Emerging trends or risks not yet critical but needing monitoring
                - Blind spots in current tracking (e.g., no data on facility uptime or skill readiness)
                - External dependency risks:
                    • Vendor instability
                    • Regulatory changes
                    • Market disruptions (e.g., supply chain or geopolitical shifts)

            7. Appendices (Optional)
                - Static rule thresholds and scoring logic used
                - Detailed transaction logs or risk flags
                - Resource availability graphs or tables
                - Burn-down charts or sprint reports
                - Any custom insights or logs helpful for audits

            Formatting Guidelines:
            - Use clear section headings in plain text (no markdown).
            - Use bullet points and numbered lists to improve readability.
            - Ensure consistent indentation and spacing for legibility.
            - Align all risk levels with appropriate symbols and numeric scores.
            - Do not use HTML, JSON, or markup in the output. Only human-readable .txt format.


            The txt file should NOT include the markdown symbols in the output (like **, #, ---). The report should be structured and easy to read, with clear headings and subheadings for each section. Use bullet points or numbered lists where appropriate to enhance readability.
            """,
            output_file="output/overall_project_risk_analysis.txt",
            agent=self.agent(),
            verbose=True
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            name="Overall Project Risk Analysis Crew",
            description="A crew specialized in analyzing project details for risk assessment.",
            agents=[self.agent()],
            tasks=[self.task()],
            process = Process.sequential,
            verbose=True
        )
    
if __name__ == "__main__":
    with open("output/project_risk_analysis.txt", "r") as f:
        project_risks = f.read()
    with open("project_details/static_rules.json", "r") as f:
        static_records = json.load(f)
        static_records = static_records["overall_risk_rules"]
    with open("output/resource_risk_analysis.txt", "r") as f:
        resources_risks = f.read()
    with open("output/transaction_risk_analysis.txt", "r") as f:
        transaction_risks = f.read()
    OverallRiskAnalysisCrew().crew().kickoff({"project_risks": project_risks, "static_records": static_records, "resources_risks": resources_risks, "transaction_risks": transaction_risks})
