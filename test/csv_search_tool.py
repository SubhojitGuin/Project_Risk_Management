from crewai_tools import CSVSearchTool
from crewai import Agent , Task , Crew , Process
from tools.rag_tool import RAGCSVTool

csv_search_agent = Agent(
    role="CSV Search Agent",
    goal="Search for all transactions made in USD in CSV files",
    backstory="An expert in searching for data in CSV files",
    verbose=True
)

def return_csv_search_tool(csv:str) -> CSVSearchTool:
    return Task(
        description="Search for all transactions made in USD in CSV files",
        expected_output="A summary of the relevant data found in the CSV files.",
        agent=csv_search_agent,
        tools=[RAGCSVTool(csv_path = csv)],
        verbose=True
    )

def return_csv_search_crew(csv:str) -> Crew:
    return Crew(
        agents=[csv_search_agent],
        tasks=[return_csv_search_tool(csv)],
        process=Process.sequential,
        verbose=True
    )

crew = return_csv_search_crew(csv = r'C:\MyProjects\Project_Risk_Management\test\business_transactions.csv')
crew_output = crew.kickoff()
print(crew_output.tasks_output)