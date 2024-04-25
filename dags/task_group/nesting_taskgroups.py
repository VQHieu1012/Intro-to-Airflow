"""
For example when building ETL, when calling API endpoints, we may need
to process new records for each endpoint before we can process update to them.
"""

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime
from airflow.utils.task_group import TaskGroup

with DAG('nesting_taskgroup',
        start_date = datetime(2024, 4, 24),
        schedule_interval = '@daily',
        catchup = False, tags=['taskgroup']) as dag:
    
    groups = []

    for g_id in range(1, 3):
        with TaskGroup(group_id=f'group{g_id}') as tg1:
            t1 = EmptyOperator(task_id='task1')
            t2 = EmptyOperator(task_id='task2')

            sub_groups = []
            for s_id in range(1, 3):
                with TaskGroup(group_id=f'sub_group{s_id}') as tg2:
                    st1 = EmptyOperator(task_id='task1')
                    st2 = EmptyOperator(task_id='task2')

                    st1 >> st2
                    sub_groups.append(tg2)
            
            t1 >> sub_groups >> t2
            groups.append(tg1)

    
    groups[0] >> groups[1]