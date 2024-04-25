from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG('share_xcom_tradi_deco', start_date=datetime(2024, 4, 25), schedule='@once', tags=['taskflow_api', 'share_xcom']):
    start = PythonOperator(
        task_id='start',
        python_callable = lambda: 42
    )

    @task
    def print(value: int): 
        return f'value from previous task {value}'

    print(value = start.output)
