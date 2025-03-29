import boto3
import os
from dotenv import load_dotenv
load_dotenv()
 
# Creating an S3 access object
PUBLIC_BUCKET = os.getenv("PUBLIC_BUCKET")
REGION = os.getenv("REGION")
def list_subfolders(bucket_name, prefix=''):
    s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name= REGION
)
    paginator = s3_client.get_paginator('list_objects_v2')
    result = set()  # Use a set to avoid duplicates
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix, Delimiter='/'):
        if 'CommonPrefixes' in page:
            for prefix in page['CommonPrefixes']:
                result.add(prefix['Prefix'])
    return list(result)

bucket_name = 'projectrisk36879'
subfolders = list_subfolders(bucket_name)
for folder in subfolders:
    print(folder)