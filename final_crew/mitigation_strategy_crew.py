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
class MitigationStrategiesAnalysisCrew:
    @agent
    def agent(self) -> Agent:
        return Agent(
            role="""
            Mitigation Strategies Analysis Agent specialized in identifying and analyzing potential mitigation strategies for various risk scenarios.
            """,
            goal="""
            Your goal is to provide a comprehensive analysis of potential mitigation strategies for the identified risks details provided in {risk_analysis} to generate relevant and effective mitigation strategies. Your analysis should include a detailed report on each strategy, its feasibility, and its potential impact on the project.
            """,
            backstory="""
            You are a seasoned risk management expert with extensive experience in identifying and mitigating risks in complex projects. You have a deep understanding of various risk scenarios and the strategies that can be employed to mitigate them. Your role is to analyze the identified risks and provide a comprehensive report on potential mitigation strategies, consider the risk details provided in {risk_analysis}. You will leverage your knowledge and expertise to provide mitigation strategies to ensure that the project is well-prepared to handle any potential risks.
            """,
            llm=llm,
            verbose=True,
        )

    @task
    def task(self) -> Task:
        return Task(
            name="Mitigation Strategies Analysis",
            description="""
            Analyze the identified risks in {risk_analysis} and generate a comprehensive report on potential mitigation strategies. The analysis should include a detailed examination of each strategy, its feasibility, and its potential impact on the project. The report should be structured and easy to read, with clear headings and subheadings for each section.
            """,
            expected_output = """
            A txt file containing a detailed report on the mitigation strategies analysis for the risk details in {risk_analysis} including the following sections but not limited to:

            - Risk Identification: List of identified risks(4-5) and their descriptions for all three categories Transaction , Resources and Project.
            - Mitigation Strategies: Detailed analysis of potential mitigation strategies for each identified risk.
            - Feasibility: Assessment of the feasibility of each mitigation strategy, including resource requirements and potential challenges.
            - Impact Analysis: Evaluation of the potential impact of each mitigation strategy on the project, including benefits and drawbacks.
            - Recommendations: Suggested course of action based on the analysis, including prioritization of mitigation strategies and next steps.
            - Conclusion: Summary of the analysis and final recommendations.

            Strategic Recommendations

                Objective:
                You must recommend appropriate mitigation actions aligned with the severity and urgency of risks you've identified.

                What You Should Do:

                - Short-Term Actions (1–7 Days):
                - Recommend immediate fixes for high-severity risks.
                - These may include patching vulnerabilities, restoring access controls, or reassigning overloaded teams.

                - Mid-Term Actions (1–4 Weeks):
                - Propose tactical adjustments like team reshuffling, process improvements, or updated sprint plans.
                - Base this on recurring issues or bottlenecks you detect.

                - Long-Term Strategies (4+ Weeks):
                - Suggest structural or policy changes when patterns indicate persistent or systemic risks.
                - Examples include introducing automation, updating compliance frameworks, or redefining project governance.

                - Assign Risk Owners:
                - For each major risk area, determine and assign responsible owners (teams or individuals) based on project metadata or previous resolution patterns.

            The txt file should NOT include the markdown symbols in the output (like **, #, ---). The report should be structured and easy to read, with clear headings and subheadings for each section. Use bullet points or numbered lists where appropriate to enhance readability.
            """,
            output_file = "output/mitigation_strategies.txt",
            agent =self.agent(),
            verbose = True
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            name="Mitigation Strategies Analysis Crew",
            description="""
            A Crew specialized in analyzing and generating mitigation strategies for various risk scenarios.
            """,
            tasks=[self.task()],
            agent = [self.agent()],
            processes=Process.sequential,
            verbose = True)
    

if __name__ == "__main__":
    with open("output/overall_project_risk_analysis.txt", "r") as f:
        risk_analysis = f.read()
        
    crew = MitigationStrategiesAnalysisCrew().crew()
    crew.kickoff({"risk_analysis": risk_analysis})