import boto3
from botocore.client import Config


from creds import (
    s3_minio_access_key,
    s3_minio_bucket_name,
    s3_minio_endpoint,
    s3_minio_secret_key,
)

S3_CONFIGS = {
    "minio": {
        "target": "minio",
        "endpoint": s3_minio_endpoint,
        "access_key": s3_minio_access_key,
        "secret_key": s3_minio_secret_key,
        "bucket": s3_minio_bucket_name,
        "secure": False,  # локально часто http
        "region": None,
    },
}

def boto3_create_bucket(conn_params: dict, bucket_name: str) -> None:
    """
    Ручка для создания бакета.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :return: Ничего.
    """
    s3 = boto3.client(conn_params)
    try:
        params = {"Bucket": bucket_name}
        if conn_params.get("region") and conn_params.get("region") != "us-east-1":
            params["CreateBucketConfiguration"] = {"LocationConstraint": conn_params["region"]}
        s3.create_bucket(**params)
        print(f"🪣 With Boto3 client; Bucket '{bucket_name}' created! in {conn_params['target']}")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"🪣 With Boto3 client; Bucket '{bucket_name}' already exists in {conn_params['target']}.")
    except Exception as e:  # noqa: BLE001
        print(f"🪣 With Boto3 client; Error creating bucket: {e} in {conn_params['target']}")


def boto3_remove_bucket(conn_params: dict, bucket_name: str) -> None:
    """
    Ручка для удаления бакета.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :return: Ничего.
    """
    s3 = boto3.client(conn_params)
    # Перед удалением бакет должен быть пустым
    resp = s3.list_objects_v2(Bucket=bucket_name)
    if "Contents" in resp and len(resp["Contents"]) > 0:
        print(f"🪣 With Boto3 client; Bucket '{bucket_name}' is not empty in {conn_params['target']}. Cannot remove.")
        return
    try:
        s3.delete_bucket(Bucket=bucket_name)
        print(f"🪣 With Boto3 client; Bucket '{bucket_name}' removed from {conn_params['target']}!")
    except Exception as e:  # noqa: BLE001
        print(f"🪣 With Boto3 client; Error removing bucket: {e} in {conn_params['target']}")


def boto3_upload_csv(conn_params: dict, bucket_name: str, object_name: str, file_path: str) -> None:
    """
    Ручка для загрузки файла в бакет.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :param object_name: Имя файла в бакете.
    :param file_path: Имя файла на диске.
    :return: Ничего.
    """
    if conn_params.get("target") == "vk":
        # VK Cloud лучше работает с Minio клиентом
        minio_upload_csv(
            conn_params=conn_params,
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
        )
    else:
        s3 = boto3.client(conn_params)
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"🪣 With Boto3 client; Uploaded {object_name} to {bucket_name} in {conn_params['target']}")


def boto3_list_objects(conn_params: dict, bucket_name: str) -> None:
    """
    Ручка для просмотра содержимого бакета.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :return: Ничего.
    """
    s3 = boto3.client(conn_params)
    resp = s3.list_objects_v2(Bucket=bucket_name)
    print(f"🪣 With Boto3 client; Objects in bucket '{bucket_name}' in {conn_params['target']}:")
    for obj in resp.get("Contents", []):
        print(obj["Key"], obj["Size"], obj["LastModified"])