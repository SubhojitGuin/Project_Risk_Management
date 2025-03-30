from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from tools.serper_tool import SearchTool
from crewai_tools import SerperDevTool
from datetime import datetime
from pydantic import BaseModel

year = datetime.now().year

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
class MarketAnalysis:
    @agent
    def agent(self) -> Agent:
        # Perform a search on the CSV file
        return Agent(
            role="Market Research Agent specializing in searching and tracking external factors impacting project lifecycles",
            goal="""
                    Continuously track and search external risks—such as economic shifts, political changes, legal regulations, environmental issues, technological advancements, market trends and geopolitical risks—that could disrupt project timelines, budgets, and outcomes. Deliver latest data to help decision-makers understand external risks that can impact project lifecycles.
                """,
            backstory="""
                    With 20+ years of experience, you were designed as an advanced AI Agent to help organizations identify uncertainty in project lifecycle. With access to latest data sources, you specialize in searching early warning signals of project risks. Over years of searching latest data on market trends, regulatory changes, economic shifts and geopolitical risks, you've developed a deep searching capability of how external risks unfold and impact projects. Your strength lies in searching latest data points that empowers businesses to stay ahead of emerging challenges.
                """,
            verbose=True
        )

    @task
    def task(self) -> Task:
        # Perform a search on the CSV file
        return Task(
            description=f"""
                Search latest data on key external factors that can impact a project's lifecycle. Specifically, research:

                1. Economic factors - global economic downturn {year}, inflation impact on businesses {year}, interest rates in {year}, currency fluctuations in {year}

                2. Political factors - political instability effects on economy {year}, new government policies affecting businesses {year}, trade restrictions {year}, regulatory changes {year}

                3. Environmental & Social factors - climate change business risks in {year}, natural disasters affecting supply chains in {year}, social unrest impact on businesses in {year}

                4. Technological factors - AI regulation impact on tech industry in {year}, cybersecurity threats in {year}, data privacy laws impacting businesses in{year}

                5. Market & Industry factors - stock market volatility in {year}, industry-specific trends affecting project lifecycles in {year}, consumer behavior changes in {year}, emerging markets in {year}

                6. Geopolitical factors - geopolitical tensions affecting trade in {year}, international relations impact on businesses in {year}, sanctions and embargoes affecting project lifecycles in {year}
                
                7. Legal factors - new business regulations {year}, legal compliance challenges for companies in {year}, intellectual property laws affecting innovation in {year}, labor laws impacting project lifecycles in {year}


                For each factor, collect data on recent trends, news and potential business impacts based on the latest data available. Also include numerical data and statistics to support your findings. The goal is to provide a comprehensive report that can help decision-makers understand the external risks that can impact project lifecycles.
            """,
            expected_output="""
                A comprehensive report detailing the latest data (4-5 points per category) on key external factors impacting project lifecycles. The report should include:
                - A detailed report of each risk factor with supporting data and latest news with numerical data and statistics to support findings
                - A timeline of key events and trends related to each risk factors with month and year 
                - A summary of the potential business risks and opportunities associated with each factor
            """,
            output_file="static_db/market_analysis_summary.json",
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
            tasks=[self.task()],
            agents=[self.agent()],
            process=Process.sequential,
            verbose=True,
        )
    

if __name__ == "__main__":
    crew = MarketAnalysis().crew()
    crew.kickoff()

