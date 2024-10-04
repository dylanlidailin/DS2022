#!/usr/local/bin/bash
import boto3
import requests
from botocore.exceptions import NoCredentialsError, ClientError

#fetch url
def fetch_file(url, local_file):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_file, 'wb') as f:
                f.write(response.content)
            print(f"File downloaded successfully as {local_file}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading file: {e}")

#upload the file to S3
def upload_to_s3(file_name, bucket_name, object_name=None):
    s3 = boto3.client('s3', region_name='us-east-1')
    
    if object_name is None:
        object_name = file_name

    try:
        with open(file_name, 'rb') as f:
            s3.put_object(
                Body=f,
                Bucket=bucket_name,
                Key=object_name,
                ACL='public-read'
            )
        print(f"File uploaded successfully to S3 bucket '{bucket_name}' as '{object_name}'")
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
    except NoCredentialsError:
        print("AWS credentials not available. Make sure your AWS credentials are configured.")
    except ClientError as e:
        print(f"Failed to upload to S3: {e}")

#generate a presigned URL
def generate_presigned_url(bucket_name, object_name, expires_in=604800):
    s3 = boto3.client('s3')
    try:
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expires_in
        )
        return presigned_url
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None

if __name__ == "__main__":
    # Step 1: Input URL and other details
    url = input("Input the URL of the file to download: ")
    local_file = "downloaded_file.gif"	
    bucket_name = input("Please enter your S3 bucket name: ")
    object_name = input("Please enter the name to save the file as in S3:  ")

    # Step 2: Download the file from the internet
    fetch_file(url, local_file)

    # Step 3: Upload the file to S3
    upload_to_s3(local_file, bucket_name, object_name)

    # Step 4: Generate a presigned URL
    presigned_url = generate_presigned_url(bucket_name, object_name)

    if presigned_url:
        print(f"Presigned URL: {presigned_url}")

