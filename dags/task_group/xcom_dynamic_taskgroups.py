from airflow import DAG
from datetime import datetime
from airflow.decorators import task_group, task, dag

@dag(schedule=None, start_date=datetime(2024, 4, 24), catchup=False)
def task_group_dynamic_mapping():

    @task
    def random_list():
        import random
        my_num = []
        for x in range(random.randint(3, 12)):
            my_num.append(x + random.randint(10, 100))
        return my_num
    
    @task_group(group_id="group1")
    def tg1(my_num):
        @task
        def print_num(num):
            return num
        
        @task
        def add_42(num):
            return num + 42
        
        print_num(my_num) >> add_42(my_num)
    
    @task
    def pull_xcom(**content):
        pulled_xcom = content["ti"].xcom_pull(
            task_ids = ["group1.add_42"],
            map_indexes = [2, 3],
            key = "return_value"
        )

        print(pulled_xcom)

    # with expand, for each value from my_num, we will create a task group objects
    # and pass each number to the my_num parameter.
    tg1_object = tg1.expand(my_num=random_list())

    tg1_object >> pull_xcom()

    dag = task_group_dynamic_mapping()