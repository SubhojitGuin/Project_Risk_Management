from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool
from datetime import datetime
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


llm = LLM(
    model=os.getenv("MODEL"),
    temperature=0.5,
    base_url="https://api.openai.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)


# Define the Result format
class Result(BaseModel):
    description: str
    date: str
    impact: str
    business_risks: str
    opportunities: str

    
class Results(BaseModel):
    category: str
    category_description: str
    data: list[Result]
    
class ResultList(BaseModel):
    results: list[Results]

@CrewBase
class MarketAnalysisCrew:
    @agent
    def agent(self) -> Agent:
        return Agent(
            role="Market Research Risk Intelligence Agent specialized in identifying and tracking external risk factors that can impact project lifecycles.",
            goal="""
                    Continuously monitor and research key external risks—economic shifts, political changes, legal regulations, environmental and social issues, technological advancements, market and industry dynamics, geopolitical risks, and resource availability—that may disrupt or influence project timelines, budgets, and outcomes. Use the provided {project_docs} to generate precise, contextual search queries (in plain string format) and collect the latest data accordingly.

                    Note:
                    - All search queries must be generated in string format only.
                    - The search queries should be tailored to the specific project location, domain, timeline, description, resources and other factors in {project_docs}.
                    - Each search query should be unique to the respective external risk factor.
                    - Perform a unique search for each factor using relevant keywords derived from the project_docs.
                    - Ensure all findings are current, relevant, and localized (if applicable).
                    
                    You MUST generate search queries one by one and wait for the response of the previous query before generating the next search query.
                """,
            backstory="""
                    With over 20 years of experience in tracking external risks, you are a seasoned research specialist who helps organizations navigate uncertainty in project planning and execution. You possess expert-level capabilities in sourcing early warning signals from real-time data across economic trends, regulatory developments, technological shifts, and geopolitical events. Your unique strength lies in uncovering emerging threats and opportunities that impact projects by leveraging your deep contextual analysis skills and an extensive understanding of how risks unfold across global landscapes. You are highly adept at producing evidence-based insights that inform critical business decisions using the provided {project_docs}.
                """,
            llm=llm,
            verbose=True
        )

    @task
    def task(self) -> Task:
        # Perform a search on the CSV file
        return Task(
            description="""
                Using the given Project Document, research and report on the latest data related to the following external risk categories. For each, generate search queries in plain string format and collect up-to-date data including recent events, statistics, news, and their potential business impacts. Tailor every search query based on the specific project location, domain, timeline, description, resources and other factors provided in {project_docs}.
                
                Analyze the following external factors:

                1. Economic Factors {year}
                2. Political Factors {year}
                3. Environmental & Social Factors {year}
                4. Technological Factors {year}
                5. Market & Industry Factors {year}
                6. Geopolitical Factors {year}
                7. Legal Factors {year}
                8. Resource Availability {year}
            """,
            expected_output="""
                A comprehensive, insight-rich report containing:

                1. Per-Factor Analysis:

                    - 2–3 current, relevant data points (news, reports, statistics) per factor
                    - Numerical data to support findings
                    - Impact analysis related to the provided project_docs

                2. Timeline of Events:

                    - Chronological list of key external events affecting each risk factor
                    - Format: Month, Year – Event Summary

                3. Risk & Opportunity Summary:

                    - Clear outline of potential risks and opportunities arising from each factor in relation to the project
            """,
            output_file="project_details/market_analysis_summary.json",
            agent=self.agent(),
            tools=[SerperDevTool()],
            output_json=ResultList,
            verbose=True
        )
    
    @crew
    def crew(self) -> Crew:
        # Create a crew with the agent and task
        return Crew(
            name="Market Analysis Crew",
            description="A crew to analyze market data in the Internet.",
            tasks=self.tasks,
            agents=self.agents,
            process=Process.sequential,
            verbose=True,
        )
    

if __name__ == "__main__":
    crew = MarketAnalysisCrew().crew()
    # Load the project description file
    with open("project_details/project_description.txt", "r") as f:
        project_description = f.read()
    
    crew.kickoff({"project_docs": project_description, "year": datetime.now().year})