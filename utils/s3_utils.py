from minio import Minio
from minio.error import InvalidResponseError, S3Error

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

def minio_create_bucket(conn_params: dict, bucket_name: str) -> None:
    """
    Ручка для создания бакета.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :return: Ничего.
    """
    client = minio_client(conn_params)
    try:
        client.make_bucket(bucket_name)
        print(f"🦩 With Minio client; Bucket '{bucket_name}' created in {conn_params['target']}!")
    except (S3Error, InvalidResponseError) as exc:
        msg = str(exc)
        if (
            (hasattr(exc, "code") and getattr(exc, "code", None) in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"))
            or "BucketAlreadyOwnedByYou" in msg
            or "BucketAlreadyExists" in msg
        ):
            print(f"🦩 With Minio client; Bucket '{bucket_name}' already exists in {conn_params['target']}.")
        else:
            print(f"🦩 With Minio client; Error creating bucket '{bucket_name}' in {conn_params['target']}: {exc}")

def minio_remove_bucket(conn_params: dict, bucket_name: str) -> None:
    """
    Ручка для удаления бакета.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :return: Ничего.
    """
    client = minio_client(conn_params)
    found = client.bucket_exists(bucket_name)
    if found:
        # Перед удалением бакет должен быть пустым
        objects = list(client.list_objects(bucket_name))
        if objects:
            print(f"🦩 With Minio client; Bucket '{bucket_name}' is not "
                  f"empty in {conn_params['target']}. Cannot remove.")
            return
        client.remove_bucket(bucket_name)
        print(f"🦩 With Minio client; Bucket '{bucket_name}' removed from {conn_params['target']}!")
    else:
        print(f"🦩 With Minio client; Bucket '{bucket_name}' does not exist in {conn_params['target']}.")

def minio_upload_csv(conn_params: dict, bucket_name: str, object_name: str, file_path: str) -> None:
    """
    Ручка для загрузки файла в бакет.

    :param conn_params: Параметры подключения.
    :param bucket_name: Имя бакета.
    :param object_name: Имя файла в бакете.
    :param file_path: Имя файла на диске.
    :return: Ничего.
    """
    client = minio_client(conn_params)
    result = client.fput_object(
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=file_path,
    )
    print(f"🦩 With Minio client; Uploaded {object_name} "
          f"to {bucket_name} in {conn_params['target']} (etag: {result.etag})")