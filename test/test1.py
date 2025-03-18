from composio import ComposioToolSet, App
import os
from dotenv import load_dotenv
load_dotenv()

# Example usage
toolset = ComposioToolSet(api_key=os.getenv('COMPOSIO_API_KEY'))
connection = toolset.get_connected_account(os.getenv('COMPOSIO_CONNECTED_ACCOUNT_ID'))
print(connection)