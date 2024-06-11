from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

with DAG(
    'external_python_env_2', schedule=None, start_date=datetime(2024, 5, 8),
    catchup=False, tags=['external_python_operator']
) as dag:
    @task.external_python(task_id="external_python",
                          python="/home/astro/.pyenv/versions/my_special_virtual_env/bin/python")
    def callable_external_python():
        import subprocess
        import os
        import sys
        cmd = 'dbt'
        args = '--version'
        temp = subprocess.Popen([cmd, args], stdout=subprocess.PIPE)
        output = str(temp.communicate())

        print(output)
        print(sys.version)
        return "A complex dependency generated value"

    task_external_python = callable_external_python()