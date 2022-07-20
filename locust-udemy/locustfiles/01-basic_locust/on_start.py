from locust import User, between, task

"""on_start and on_stop methods are executed one time per user simulated, but only runs at the begining and end of the execution
"""
class MyUser(User):
    
    wait_time = between(1, 3)
    host = "www.google.com"
    
    def on_start(self):
        print("Login")
        
    @task
    def doing_work(self):
        print("Doing work")

    def on_stop(self):
        print("Logout")
        
