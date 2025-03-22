from composio_crewai import ComposioToolSet
from crewai.tools import BaseTool
import os
from dotenv import load_dotenv
from crewai_tools import QdrantVectorSearchTool
from pydantic import Field
import os
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# -- Jira Tool --
composio_toolset = ComposioToolSet(api_key=os.getenv('COMPOSIO_API_KEY'))
jira_tool = composio_toolset.get_tools(actions=['JIRA_SEARCH_FOR_ISSUES_USING_JQL_GET'])
# jira_tool.get_issues(jql="project = 'CREWS' AND status = 'In Progress'")


#-- Qdrant Tool --
def get_qdrant_tool(qdrant_collection_name: str) -> QdrantVectorSearchTool:
    return QdrantVectorSearchTool(
        qdrant_url=os.getenv("QDRANT_URL"),
        qdrant_api_key=os.getenv("QDRANT_API_KEY"),
        collection_name= qdrant_collection_name
    )


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