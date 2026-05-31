from minio import Minio

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

def minio_client(conn_params: dict) -> Minio:
    """
    Создает экземпляр Minio.

    :param conn_params: Параметры подключения.
    :return: Клиент Minio.
    """
    return Minio(
        endpoint=conn_params["endpoint"],
        access_key=conn_params["access_key"],
        secret_key=conn_params["secret_key"],
        secure=conn_params.get("secure", True),
    )

def minio_list_buckets(conn_params: dict) -> None:
    """
    Отображает список бакетов.

    :param conn_params: Параметры подключения.
    :return: Ничего.
    """
    client = minio_client(conn_params)
    buckets = client.list_buckets()
    print(f"🦩 With Minio client; Buckets (minio) in {conn_params['target']}:")
    for bucket in buckets:
        print(bucket.name, bucket.creation_date)