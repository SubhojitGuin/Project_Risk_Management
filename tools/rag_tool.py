import pandas as pd
import numpy as np
from dotenv import load_dotenv
from crewai.tools import BaseTool
from pydantic import Field, ConfigDict
from langchain.document_loaders import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os

# Load environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

class RAGCSVTool(BaseTool):
    name: str = "RAG from CSV"
    description: str = "Retrieves relevant information from a CSV file using semantic search."
    csv_path: str = Field(..., description="Path to the CSV file")
    db: Chroma = None # Field(default=None, description="Chroma database for semantic search")
    
    model_config = ConfigDict(arbitrary_types_allowed=True)  # Allow non-Pydantic types

    def __init__(self, csv_path: str):
        super().__init__(csv_path=csv_path)
        self.csv_path = csv_path
        self.db = self._create_db()

    def _csv_loader(self):
        loader = CSVLoader(self.csv_path, encoding="utf-8")
        df = loader.load()
        return df

    def _create_db(self):
        embedding_function = OpenAIEmbeddings()
        db = Chroma.from_documents(self._csv_loader(), embedding_function)
        return db
    
    def _run(self, query: dict) -> str:
        """Retrieve the most relevant row from the CSV based on the query."""
        if isinstance(query, dict):  # Handle incorrect input
            query = query.get("description", "")  # Extract the actual string from the dictionary
            if not query:
                return "Invalid query format. Expected a string."
        results = self.db.similarity_search(query, k=10)
        if not results:
            return "No relevant information found."
        return "\n\n".join(result.page_content for result in results)