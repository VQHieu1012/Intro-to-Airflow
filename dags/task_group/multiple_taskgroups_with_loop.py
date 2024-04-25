from airflow.utils.task_group import TaskGroup
from datetime import datetime
from airflow.operators.empty import EmptyOperator
from airflow import DAG

with DAG(
        'multiple_taskgroup_with_loop',
        start_date = datetime(2024, 4, 24),
        schedule_interval='@daily',
        catchup=False, tags=['taskgroup']) as dag:
    
    groups = []

    for g_id in range(1, 4):
        tg_id = f'group{g_id}'
        with TaskGroup(group_id=tg_id) as tg1:
            t1 = EmptyOperator(task_id='task1')
            t2 = EmptyOperator(task_id='task2')

            t1 >> t2

            if tg_id == 'group1':
                t3 = EmptyOperator(task_id='task3')

                t1 >> t3
            
            groups.append(tg1)
    
    [groups[0], groups[1]] >> groups[2]