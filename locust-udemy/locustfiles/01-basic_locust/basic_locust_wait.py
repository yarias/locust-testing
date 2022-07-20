from locust import HttpUser, task, between, constant, constant_pacing
from datetime import datetime

class BaiscHttpUser(HttpUser):
    
    # wait_time=between(1, 3)
    # wait_time=constant(3)
    wait_time=constant_pacing(5) # waits X seconds to execute the next task: task1_time + wait1_time = task2_time + wait2_time. task_time>cnst_pacing_time then wait time = 0
    host="www.google.com"
    
    @task
    def get_root(self):
        print(datetime.now())
