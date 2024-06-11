from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import sys

with DAG('external_python_env_1', start_date=datetime(2024, 5, 8),
         schedule=None, catchup=False, tags=['external_python_operator']) as dag:
    
    @task.external_python(task_id="external_python", python="/home/astro/.pyenv/versions/my_special_virtual_env/bin/python")
    def callable_external_python():
        print(sys.version)
        return 'A complex dependency generated value'