from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import TextLoader


load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

def get_text_loader(path_list):
    """Load text files from a list of paths."""
    document_loader = []
    for path in path_list:
        loader = TextLoader(path)
        document_loader.extend(loader.load())
    return document_loader

def get_text_chunks(docs):
    chunks = []
    for doc in docs:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000 , chunk_overlap =100)
        chunks += text_splitter.split_text(doc.page_content)
    return chunks

def get_vector_store(path_list):
    """Create a vector store from text files."""

    docs = get_text_loader(path_list)
    text_chunks = get_text_chunks(docs)
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding = embeddings)
    vector_store.save_local("vector_store")
    return vector_store

def get_conversational_chain():
    prompt_template = """
    You are an answering assistant for a project report.
    Your task is to answer the question based on the provided context.
    Answer the following question in a very detailed manner based only on the provided context. 
    You should not answer anything outside the context.
    Remove any markdown formatting from the answer.
    
    
    <context>
    {context}
    </context>
    Question: {question}"""

    
    llm = ChatOpenAI(model=os.getenv("MODEL"), temperature=0.25)
    prompt = PromptTemplate(template = prompt_template , input_variables={"context","question"})
    chain = load_qa_chain(llm , chain_type="stuff" , prompt=prompt)
    return chain

def get_answer_from_chain(question : str):
    db = FAISS.load_local("vector_store", OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    context = db.similarity_search(question, k=5)
    chain = get_conversational_chain()
    answer = chain.invoke({"input_documents": context, "question": question})
    return answer


if __name__ == "__main__":
    path_list = ["output/report.txt", "output/mitigation_strategies.txt"]
    vector_store = get_vector_store(path_list)
    question = "Provide the details of all the risks identified as critical and High severity risks in the project report."
    answer = get_answer_from_chain(question)
    print(answer["output_text"])

# Answer the following question in a detailed manner based only on the provided context. 
#     Think step by step before providing an answer,make sure to provide all the details
#     I will tip you $1000 if the user finds the answer helpful.
#     if the answer is not in provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n 