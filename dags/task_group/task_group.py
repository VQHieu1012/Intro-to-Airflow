from airflow.utils.task_group import TaskGroup
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

with DAG(
    'basic_task_group',
    schedule_interval = '@daily',
    start_date = datetime(2022, 1, 1),
    catchup = False, tags=['taskgroup']
) as dag:
    t0 = EmptyOperator(task_id='start')

    with TaskGroup(group_id='group1') as tg1:
        t1 = EmptyOperator(task_id='task1')
        t2 = EmptyOperator(task_id='task2')

        t1 >> t2
    
    t3 = EmptyOperator(task_id='task3')

    # task dependencies
    t0 >> tg1 >> t3

"""
When your task is within a Task Group, your callable task_id will be the task_id prefixed with the group_id 
(i.e. group_id.task_id). 
This ensures the uniqueness of the task_id across the DAG.
This is important to remember when calling specific tasks with XCOM passing or branching operator decisions.
"""