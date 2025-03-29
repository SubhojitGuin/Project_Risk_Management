from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai_tools import CSVSearchTool

@CrewBase
class CSVSearch:
    def __init__(self, **kwargs):
        self.csv_path = kwargs.get('csv_path', None)
        self.search_query = kwargs.get('search_query', None)
    
    @agent
    def agent(self):
        # Perform a search on the CSV file
        return Agent(
            role="CSV Analyzer Agent",
            goal="Analyze the relevant data in CSV files and find the transactions made in USD.",
            backstory="An expert in analyzing the transactions made in USD in CSV files and summarizing it",
            verbose=True
        )
    
    @task
    def task(self):
        # Perform a search on the CSV file
        return Task(
            description="Analyze the relevant data in CSV files and summarize the transactions made in USD.",
            expected_output="A summary of the relevant transactions made in USD in the CSV files.",
            agent=self.agent(),
            tools=[CSVSearchTool(csv=self.csv_path , search_query=self.search_query)],
            verbose=True
        )

    @crew
    def csv_search_crew(self):
        # Perform a search on the CSV file
        return Crew(
            agents=[self.agent()],
            tasks=[self.task()],
            process=Process.sequential,
            verbose=True
        )   

obj = CSVSearch(
        csv_path = r'Download\DownloadedFile.csv',
        search_query = "List the transactions made in USD"
    )
crew_output = obj.csv_search_crew().kickoff()
print(crew_output.tasks_output)