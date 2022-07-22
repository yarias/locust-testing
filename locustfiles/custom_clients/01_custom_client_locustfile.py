from locust import SequentialTaskSet, task, between
from locustfiles.custom_clients.custom_client.custom_client import CustomLocust


class UserBehaviour(SequentialTaskSet):
    @task
    def my_task1(self):
        self.client.custom_req_conn()
        return None
        
    @task
    def my_task2(self):
        self.client.custom_send_conn()
    
    @task
    def my_task3(self):
        self.client.custom_req_discnn()
        

class MyUser(CustomLocust):
    tasks = [UserBehaviour]
    wait_time = between(2, 5)
    host = "google.com"