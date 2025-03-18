
from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from crewai.tools import BaseTool
from pydantic import Field
import json
import os
from crewai_tools import QdrantVectorSearchTool
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# -- Search Tool --
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


# -- Market Analysis Agent --
market_research_agent = Agent(
    role='Market Research Analyst for stock market, crypto, forex and exchange rates of the Indian market',
    goal='Gather current market data and trends',
    backstory="""You are an expert research analyst with 10 years of experience in gathering latest market finance trends, stocks and forex about Indian market. You're known for your ability to find relevant and up-to-date market information and present it in a clear, actionable format.""",
    tools=[SearchTool()],
    verbose=True
)

market_research_task = Task(
    description='Find the latest market news about stock market, crypto, forex and exchange rates of the Indian market',
    expected_output='A bullet list summary of the top 5 most important news based on the stock market, crypto, forex and exchange rates of the Indian market.',
    agent=market_research_agent,
    tools=[SerperDevTool()],
    verbose=True
)


# -- Semantic Search Agent --
qdrant_tool = QdrantVectorSearchTool(
    qdrant_url=os.getenv("QDRANT_URL"),
    qdrant_api_key=os.getenv("QDRANT_API_KEY"),
    collection_name=os.getenv("QDRANT_COLLECTION_NAME")
)

semantic_search_agent = Agent(
    role="Senior Semantic Search Agent",
    goal="Find and analyze documents based on semantic search",
    backstory="""You are an expert research assistant who can find relevant information using semantic search in a Qdrant database.""",
    tools=[qdrant_tool],
    verbose=True
)

semantic_search_task = Task(
    description="""Search for relevant documents about the {query}.
    Your final answer should include:
    - The relevant information found
    - The similarity scores of the results
    - The metadata of the relevant documents""",
    context=[market_research_task],
    agent=semantic_search_agent,
    verbose=True
)


# -- Transaction Risk Analysis Agent --    
transaction_risk_analysis_agent = Agent(
    role="Transaction Risk Analysis Expert",
    goal="Generate answers to '{query}' based on the context provided",
    backstory="""You are a risk analysis expert who can analyze context, metadata of relevant documents, the market research data and analyze the risks in transactions and generate answers to '{query}'.""",
    tools=[qdrant_tool],
    verbose=True
)

transaction_risk_analysis_task = Task(
    description="""Given the context and metadata of relevant documents, the market research data and the {query}
    analyze the risks involved in the transactions and generate the final answer.""",
    agent=transaction_risk_analysis_agent,
    context=[market_research_task, semantic_search_task],
    verbose=True
)


# -- Market and Transaction Risk Analysis Crew --
def return_market_and_transaction_risk_analysis_crew() -> Crew:
    return Crew(
        agents=[market_research_agent, semantic_search_agent, transaction_risk_analysis_agent],
        tasks=[market_research_task, semantic_search_task, transaction_risk_analysis_task],
        process=Process.sequential,
        output_log_file="crews/logs/market_and_transaction_risk_analysis_crew.txt",
        verbose=True
    )
