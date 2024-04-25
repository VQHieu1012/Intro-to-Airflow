from airflow import DAG
from airflow.decorators import task
from datetime import datetime

with DAG('share_xcom_decorator', start_date=datetime(2024, 4, 25), schedule='@once', tags=["taskflow_api", "share_xcom"]):
    @task
    def t1():
        return 42
    
    @task(do_xcom_push=False)
    def t2(value: int) -> dict[str, int]:
        print(value)
        return {'first_val': value, 'second_val': 42*2}
    
    @task
    def t3(first_val: int, second_val: int):
        print(first_val)
        print(second_val)
    
    values = t2(t1())

    t3(values['first_val'], values['second_val'])