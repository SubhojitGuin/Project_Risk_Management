from crewai_tools import CSVSearchTool
from crewai import Agent , Task , Crew , Process

csv_search_agent = Agent(
    role="CSV Search Agent",
    goal="Search for relevant data in CSV files",
    backstory="An expert in searching for data in CSV files",
    verbose=True
)

def return_csv_search_tool(csv:str) -> CSVSearchTool:
    return Task(
        description="Search for relevant data in the provided CSV files.",
        expected_output="A summary of the relevant data found in the CSV files.",
        agent=csv_search_agent,
        tools=[CSVSearchTool(csv = csv , search_query = "List the transactions made in USD")],
        verbose=True
    )

def return_csv_search_crew(csv:str) -> Crew:
    return Crew(
        agents=[csv_search_agent],
        tasks=[return_csv_search_tool(csv)],
        process=Process.sequential,
        verbose=True
    )

crew = return_csv_search_crew(csv = r"business_transactions.csv")
crew_output = crew.kickoff()
print(crew_output.tasks_output)