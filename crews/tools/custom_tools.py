from composio_crewai import ComposioToolSet
import os
from dotenv import load_dotenv
load_dotenv()

composio_toolset = ComposioToolSet(api_key=os.getenv('COMPOSIO_API_KEY'))
jira_tool = composio_toolset.get_tools(actions=['JIRA_SEARCH_FOR_ISSUES_USING_JQL_GET'])
# jira_tool.get_issues(jql="project = 'CREWS' AND status = 'In Progress'")
