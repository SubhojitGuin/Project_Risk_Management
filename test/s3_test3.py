import boto3
import os
from dotenv import load_dotenv
load_dotenv()
 
# Creating an S3 access object
PUBLIC_BUCKET = os.getenv("PUBLIC_BUCKET")
REGION = os.getenv("REGION")
file_key = "Me.jpg"

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name= REGION
)
# Uploading a png file to S3 in
# 'mygfgbucket' from local folder
s3.upload_file(
    Filename="business_transactions.csv",
    Bucket=PUBLIC_BUCKET,
    Key="ABC/business_transactions.csv"
)
 
s3.download_file(
    Filename="Download/DownloadedFile.csv",
    Bucket=PUBLIC_BUCKET,
    Key="ABC/business_transactions.csv"
)