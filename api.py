# -- import necessary libraries --
from typing import List, Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from utils.s3_utils import get_report_url, validate_file
from utils.rag_utils import get_answer_from_chain_qdrant
import os

os.makedirs("chat_db", exist_ok=True)
app = FastAPI()

class Project(BaseModel):
    project_id: str = Field(..., description="Project ID")

class Question(BaseModel):
    project_id: str = Field(..., description="Project ID")
    question: str = Field(..., description="Question to be answered")

@app.get("/")
async def get_root():
    return {"message": "Welcome to the AI-Powered Project Risk Analysis API!"}

@app.get("/health")
async def get_health():
    return {"status": "ok"}

@app.post("/api/v1/get_report")
async def get_response(request: Project):
    print("\n=================== Fetching Report ===================\n")
    project_id = request.project_id
    print("Project ID: " + project_id)
    
    # Fetch report url from s3
    file_key = f"{project_id}/report.txt"
    file_url = get_report_url(file_key)
    
    if not validate_file(f"{project_id}/"):
        print("Invalid Project ID: " + project_id) # Add a message to indicate that the project ID is invalid
        return JSONResponse(status_code=404, content={"error": "Invalid Project ID"})
    
    if not validate_file(file_key):
        print("Report Not Found Project ID: " + project_id) # Add a message to indicate that the report is not yet ready
        return JSONResponse(status_code=404, content={"error": "Report Not Found"})

    print("file_url: " + str(file_url))
    return {"file_url" : str(file_url)}


@app.post("/api/v1/get_answer")
async def get_answer(request: Question):
    print("\n=================== Fetching Answer ===================\n")
    project_id = request.project_id
    question = request.question
    print("Project ID: " + project_id)
    print("Question: " + question)

    # Get answer from chain
    answer = get_answer_from_chain_qdrant(question, project_id)
    print("Answer: " + answer["output_text"])
    return {"answer": answer["output_text"]}


if __name__ == "__main__":
  import multiprocessing
  import subprocess
  import uvicorn

  # workers = multiprocessing.cpu_count() * 2 + 1

  uvicorn_cmd = [
      "uvicorn",
      "api:app",
      "--host=0.0.0.0",
      "--port=8000",
      # f"--workers={workers}",
      "--reload"
  ]

  # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, workers=workers)
  subprocess.run(uvicorn_cmd)