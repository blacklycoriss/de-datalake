import boto3
from botocore.client import Config


from creds import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_DEFAULT_REGION,
    ENDPOINT_URL,
)

S3_CONFIGS = {
    "minio": {
        "target": "minio",
        "endpoint": ENDPOINT_URL,
        "access_key": AWS_ACCESS_KEY_ID,
        "secret_key": AWS_SECRET_ACCESS_KEY,
        "bucket": None,
        "secure": False,
        "region": AWS_DEFAULT_REGION,
    },
}

def get_s3_client(conn_params: dict):
    return boto3.client(
        's3',
        endpoint_url=conn_params['endpoint'],
        aws_access_key_id=conn_params['access_key'],
        aws_secret_access_key=conn_params['secret_key'],
        region_name=conn_params.get('region', 'us-east-1'),
        use_ssl=conn_params.get('secure', True),
        config=Config(signature_version='s3v4')
    )

def boto3_create_bucket(conn_params: dict, bucket_name: str) -> None:

    s3 = get_s3_client(conn_params)

    try:
        params = {"Bucket": bucket_name}
        if conn_params.get("region") != "us-east-1":
            params["CreateBucketConfiguration"] = {"LocationConstraint": conn_params["region"]}
        s3.create_bucket(**params)
        print(f"🪣 With Boto3 client; Bucket '{bucket_name}' created! in {conn_params['target']}")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"🪣 With Boto3 client; Bucket '{bucket_name}' already exists in {conn_params['target']}.")
    except Exception as e:
        print(f"🪣 With Boto3 client; Error creating bucket: {e} in {conn_params['target']}")


def boto3_remove_bucket(conn_params: dict, bucket_name: str) -> None:

    s3 = get_s3_client(conn_params)
    
    resp = s3.list_objects_v2(Bucket=bucket_name)

    if "Contents" in resp and len(resp["Contents"]) > 0:
        print(f"🪣 With Boto3 client; Bucket '{bucket_name}' is not empty in {conn_params['target']}. Cannot remove.")
        return
    
    try:
        s3.delete_bucket(Bucket=bucket_name)
        print(f"🪣 With Boto3 client; Bucket '{bucket_name}' removed from {conn_params['target']}!")
    except Exception as e:
        print(f"🪣 With Boto3 client; Error removing bucket: {e} in {conn_params['target']}")


def boto3_upload_csv(conn_params: dict, bucket_name: str, object_name: str, file_path: str) -> None:
    
    s3 = get_s3_client(conn_params)

    s3.upload_file(file_path, bucket_name, object_name)
    print(f"🪣 With Boto3 client; Uploaded {object_name} to {bucket_name} in {conn_params['target']}")


def boto3_list_objects(conn_params: dict, bucket_name: str) -> None:

    s3 = get_s3_client(conn_params)
    
    print(f"🪣 With Boto3 client; Objects in bucket '{bucket_name}' in {conn_params['target']}:")

    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get("Contents", []):
            print(obj["Key"], obj["Size"], obj["LastModified"])