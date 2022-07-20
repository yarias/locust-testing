from locust import HttpUser, task, between

class BaiscHttpUser(HttpUser):
    
    wait_time=between(1, 5)
    host="www.google.com"
    
    @task
    def get_root(self):
        self.client.get("/")
