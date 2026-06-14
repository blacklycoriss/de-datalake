from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

with DAG(
    dag_id="spark_pi",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["spark"],
    description="Пример запуска Spark через SparkSubmitOperator",
) as dag:

    spark_pi_task = SparkSubmitOperator(
        task_id="spark_pi_task",
        application="/opt/spark/examples/src/main/python/pi.py",
        conn_id="spark_default",          # использует Connection из переменной окружения
        conf={
            "spark.driver.memory": "512m",
            "spark.executor.memory": "256m",
        },
        # deploy_mode и spark_home уже заданы в Connection
    )