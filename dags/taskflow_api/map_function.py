from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG('map_function', start_date=datetime(2024, 4, 25), schedule='@once', tags=['taskflow_api', 'share_xcom']):
    start = PythonOperator(
        task_id='start',
        python_callable = lambda: ['/user/dir_a', '/user/dir_b']
    )

    value = start.output.map(lambda path: path + '/data')

    @task
    def print(value: int): 
        for v in value:
            print(v)

    start >> print(value)
