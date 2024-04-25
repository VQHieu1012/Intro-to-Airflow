from airflow.decorators import dag, task
from datetime import datetime
from airflow.operators.python import get_current_context # access context

@dag(start_date=datetime(2024, 4, 25), schedule='@once', tags=['taskflow_api'])
def decorator_dag(): # decorator_dag is dag_id

    @task(retries=3) # This is Python Operator wrapper
    def start(**context):    # ti is for task instance
                             # ds is datetime for current dag run
        print(context)       # If you want to access all context variables, just add **context
        #context = get_current_context()     # another way to access context
        return 'success'
    
    @task.branch # Branch Python Operator behind the scene
    def choose_task(next_task: str):
        return next_task
    
    @task
    def success(retries=1):
        print('success')

    @task
    def failure(retries=1):
        print('failure')

    choose_task(start()) >> [success(), failure()]

decorator_dag()