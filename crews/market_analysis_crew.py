
from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from crewai.tools import BaseTool
from pydantic import Field
import json
import os

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# -- Chat Model --
search = GoogleSerperAPIWrapper()

class SearchTool(BaseTool):
    name: str = "Search"
    description: str = "Useful for search-based queries. Use this to find current information about markets, companies, and trends."
    search: GoogleSerperAPIWrapper = Field(default_factory=GoogleSerperAPIWrapper)

    def _run(self, query: str) -> str:
        """Execute the search query and return results"""
        try:
            return self.search.run(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"

# Create Agents
market_research_agent = Agent(
    role='Market Research Analyst',
    goal='Gather current market data and trends',
    backstory="""You are an expert research analyst with years of experience in gathering latest market finance trends, stocks and forex. You're known for your ability to find relevant and up-to-date market information and present it in a clear, actionable format.""",
    # tools=[SearchTool()],
    verbose=True
)

# research_agent = Agent(
#     role="{topic} Research Analyst",
#     goal="Find and summarize information about the latest AI news in specific {topic} based on the uesr query",
#     backstory="You are an experienced researcher with attention to detail and a knack for finding the most important information on the {topic}.",
#     llm = os.getenv("MODEL"),
#     verbose=True  # Enable logging for debugging
# )

# Example task
task = Task(
    description='Find the latest market news on {topic}',
    expected_output='A bullet list summary of the top 5 most important news based on the {topic} .',
    agent=market_research_agent,
    tools=[SerperDevTool()],
    verbose=True
)

# Execute the crew
def return_market_analysis_crew():
    return Crew(
        agents=[market_research_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )


# crew_output = crew.kickoff(inputs = {'topic': 'Latest Market news on stocks market , crypto ,forex and exchange rates of India'})

# # Accessing the task output
# task_output = task.output

# print(f"Task Description: {task_output.description}")
# print(f"Task Summary: {task_output.summary}")
# print(f"Raw Output: {task_output.raw}")
# if task_output.json_dict:
#     print(f"JSON Output: {json.dumps(task_output.json_dict, indent=2)}")
# if task_output.pydantic:
#     print(f"Pydantic Output: {task_output.pydantic}")

# print(f"Raw Output: {crew_output.raw}")
# if crew_output.json_dict:
#     print(f"JSON Output: {json.dumps(crew_output.json_dict, indent=2)}")
# if crew_output.pydantic:
#     print(f"Pydantic Output: {crew_output.pydantic}")
# print(f"Tasks Output: {crew_output.tasks_output}")
# print(f"Token Usage: {crew_output.token_usage}")


