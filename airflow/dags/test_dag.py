# airflow/dags/test_dag.py
# Определение импортов и зависимостей для DAG
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator # type: ignore
from airflow.operators.dummy import DummyOperator # type: ignore

# Определение аргументов по умолчанию для DAG
default_args = {
    'owner': 'test_user',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
}

# Определение DAG с использованием контекстного менеджера
with DAG(
    default_args=default_args,
    dag_id="airflow_test_dag",
    tags=["python", "test"],
    description='Простой тестовый DAG',
    schedule_interval='@once',
    catchup=False,
) as dag:
# Определение функций для задач PythonOperator

    def print_start():
        print("DAG started")
        return "Start Successful"

    def print_end():
        print("DAG completed")
        return "End Successful"

# Определение задач DAG
    start = DummyOperator(task_id='start')

    task_start = PythonOperator(
        task_id='print_start',
        python_callable=print_start
    )

    task_end = PythonOperator(
        task_id='print_end',
        python_callable=print_end
    )

    end = DummyOperator(task_id='end')

# Определение последовательности выполнения задач
    start >> task_start >> task_end >> end