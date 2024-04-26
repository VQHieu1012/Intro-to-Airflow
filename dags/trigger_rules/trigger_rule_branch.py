'''
[ta, tb, tc] >> td

* All rules
1. all_success
    ta, tb, tc all succeed -> td is triggered
    ta succeeds, tb failed, tc upstream failed -> td upstream failed

2. all_failed
    ta, tb, tc all failed -> td is triggered
    ta succeeds, tb failed, tc upstream failed -> td is skipped

3. all_skipped
    ta, tb, tc all skipped -> td is triggered
    ta succeeds, tb failed, tc skipped -> td is skipped

4. all_done
    ta, tb, tc is done (don't care about the state)-> td is triggered

* One rules
1. one_success (trigger as soon as one task succeed)
    if one task succeed, td is triggered (no need to wait for all upstream tasks to be done)
    if none of the tasks succeeded, td is upstream_failed

2. one_failed (trigger as soon as one task failed)
    if one of those task failed, td is trigger (no need to wait all upstream task to bo done)
    if none of them failed, td is skipped

* None rules
1. none_failed
    if none of those tasks failed, td is triggered
    if one of those tasks failed or upstream_failed, td is skipped

2. none_failed_min_one_success
    if none of those has failed or upstream_failed and at least one task succeeded -> td is triggered
    if one of those task has failed or upstream_failed, td is skipped

3. none_skipped
    if none of those tasks skipped, td is triggered
    if one of those tasks skipped, td is skipped
'''

from airflow import DAG
from airflow.decorators import task, branch_task
from datetime import datetime

with DAG('trigger_rule_branch', start_date=datetime(2024, 4, 26),
         schedule_interval='@daily', catchup=False, tags=['trigger_rules']) as dag:

    @branch_task
    def ta():
        return 'tb'
    
    @task(trigger_rule='all_success')
    def tb():
        None
    
    @task(trigger_rule='one_failed')
    def tc():
        None

    @task(trigger_rule='none_failed')
    def td():
        None
    
    ta() >> [tb(), tc()] >> td()