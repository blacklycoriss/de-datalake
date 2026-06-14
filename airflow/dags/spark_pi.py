from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

with DAG(
    dag_id="spark_pi_docker",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["spark", "docker"],
) as dag:

    spark_pi = DockerOperator(
        task_id="spark_pi",
        image="bitnamilegacy/spark:3.5.1",
        container_name="spark-pi-runner",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="datalake-network",          # фиксированная сеть (должна существовать)
        mount_tmp_dir=False,
        command=[
            "spark-submit",
            "--master", "spark://spark-master:7077",
            "--deploy-mode", "client",
            "--conf", "spark.driver.memory=1g",
            "--conf", "spark.executor.memory=1g",
            "--conf", "spark.driver.cores=1",
            "--conf", "spark.executor.cores=1",
            "--conf", "spark.executor.instances=1",
            "--conf", "spark.driver.bindAddress=0.0.0.0",
            "--conf", "spark.driver.host=spark-pi-runner",
            "--conf", "spark.driver.port=0",
            "--conf", "spark.blockManager.port=0",
            "/opt/bitnami/spark/examples/src/main/python/pi.py"
        ],
        environment={
            "AWS_ACCESS_KEY_ID": "minioadmin",
            "AWS_SECRET_ACCESS_KEY": "minioadmin",
            "AWS_REGION": "us-east-1",
            "AWS_ENDPOINT_URL": "http://minio:9000",
        },
    )