from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

def _return_xcom(ti=None):
    ti.xcom_push(key='start', value=42)


with DAG('share_xcom_traditional', start_date=datetime(2024, 4, 25), schedule='@once', tags=['taskflow_api', 'share_xcom']):
    start = PythonOperator(
        task_id='start',
        python_callable = _return_xcom
    )

    print = BashOperator(
        task_id='print',
        bash_command = f'''echo "value from previous task {start.output} or {{ti.xcom_pull(task_id='start', key='start')}}"'''
    )

    start >> print
