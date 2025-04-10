import boto3
import os
from dotenv import load_dotenv
load_dotenv()
 
# Creating an S3 access object
PUBLIC_BUCKET = os.getenv("PUBLIC_BUCKET")
REGION = os.getenv("REGION")
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name= REGION
)

def list_subfolders(prefix=''):
    
    paginator = s3_client.get_paginator('list_objects_v2')
    result = set()  # Use a set to avoid duplicates
    for page in paginator.paginate(Bucket=PUBLIC_BUCKET, Prefix=prefix, Delimiter='/'):
        if 'CommonPrefixes' in page:
            for prefix in page['CommonPrefixes']:
                result.add(prefix['Prefix'])

    return list(result)

def download_file(file_key, local_path):
    s3_client.download_file(PUBLIC_BUCKET, file_key, local_path)

def upload_file(file_key, local_path):
    s3_client.upload_file(local_path, PUBLIC_BUCKET, file_key, ExtraArgs={'ACL': 'public-read'})

def get_report_url(file_key):
    return f"https://{PUBLIC_BUCKET}.s3.{REGION}.amazonaws.com/{file_key}"

if __name__ == "__main__":
    bucket_name = PUBLIC_BUCKET
    file_key = "IPM/report.txt"
    file_url = f"https://{PUBLIC_BUCKET}.s3.{REGION}.amazonaws.com/{file_key}"
    print(file_url)
    