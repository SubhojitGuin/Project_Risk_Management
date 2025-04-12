from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

url = os.getenv("QDRANT_URL")
api_key = os.getenv("QDRANT_API_KEY")
embeddings = OpenAIEmbeddings()

def create_qdrant_collection(docs, collection_name):
    QdrantVectorStore.from_documents(
        docs,
        embeddings,
        url=url,
        prefer_grpc=True,
        api_key=api_key,
        collection_name=collection_name,
    )

def get_qdrant_collection(collection_name):
    return QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=collection_name,
        url=url,
        api_key=api_key,
        prefer_grpc=True
    )

def delete_qdrant_collection(collection_name):
    qdrant_client = QdrantClient(
        url=url,
        api_key=api_key,
        prefer_grpc=True
    )
    qdrant_client.delete_collection(collection_name=collection_name)

if __name__ == "__main__":
    collection_name = "test_collection"
    delete_qdrant_collection(collection_name)
    print("Collection deleted successfully.")
    # create_qdrant_collection(docs, collection_name)
    # print("Collection created successfully.")