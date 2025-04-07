from s3_utils import list_subfolders, download_file, upload_file
from final_crew import MarketAnalysisCrew, MitigationStrategiesAnalysisCrew, OverallRiskAnalysisCrew, ProjectRiskAnalysisCrew, ResourceRiskAnalysisCrew, TransactionRiskAnalysisCrew
from datetime import datetime
import os
import json

os.makedirs('output', exist_ok=True)
os.makedirs('project_details', exist_ok=True)

subfolders = list_subfolders()

for folder in subfolders:
    print(f"Processing folder: {folder}")
    download_file(f"{folder}resource.json", "project_details/resource.json")
    download_file(f"{folder}project.json", "project_details/project.json")
    download_file(f"{folder}transaction.json", "project_details/transaction.json")
    download_file(f"{folder}project_description.txt", "project_details/project_description.txt")

    with open("project_details/project_description.txt", "r") as f:
        project_description = f.read()

    with open("project_details/transaction.json", "r") as f:
        transaction_records = json.load(f)

    with open("project_details/static_rules.json", "r") as f:
        static_records = json.load(f)

    with open("project_details/resource.json", "r") as f:
        resource_records = json.load(f)

    with open("project_details/project.json", "r") as f:
        project_records = json.load(f)
    
    MarketAnalysisCrew().crew().kickoff({"project_docs": project_description, "year": datetime.now().year})

    with open("project_details/market_analysis_summary.json", "r") as f:
        market_records = json.load(f)

    TransactionRiskAnalysisCrew().crew().kickoff({"transaction_records": transaction_records, "static_records": ["transaction_rules"], "market_records": market_records})
    ResourceRiskAnalysisCrew().crew().kickoff({"resource_records": resource_records, "static_records": static_records["resource_management_rules"], "market_records": market_records})
    ProjectRiskAnalysisCrew().crew().kickoff({"project_records": project_records, "static_records": static_records["project_risk_rules"]})

    with open("output/project_risk_analysis.txt", "r") as f:
        project_risks = f.read()
    with open("output/resource_risk_analysis.txt", "r") as f:
        resources_risks = f.read()
    with open("output/transaction_risk_analysis.txt", "r") as f:
        transaction_risks = f.read()
        
    OverallRiskAnalysisCrew().crew().kickoff({"project_risks": project_risks, "static_records": static_records["overall_risk_rules"], "resources_risks": resources_risks, "transaction_risks": transaction_risks})
    
    with open("output/overall_project_risk_analysis.txt", "r") as f:
        risk_analysis = f.read()
    MitigationStrategiesAnalysisCrew().crew().kickoff({"risk_analysis": risk_analysis})

    with open("output/report.txt", 'a') as f:
        f.write(f"Project: {folder}\n")
        f.write(f"Transaction Analysis: {transaction_risks}\n")
        f.write(f"Resource Analysis: {resources_risks}\n")
        f.write(f"Project Analysis: {project_risks}\n")
        f.write(f"Overall Risk Analysis: {risk_analysis}\n")
        f.write("\n\n")

    upload_file(f"{folder}report.txt", "output/report.txt")
    upload_file(f"{folder}mitigation_strategies.txt", "output/mitigation_strategies.txt")
   