from locust import User, SequentialTaskSet, task, between

"""
locust -f locustfiles/basic_taskclass_sequential.py -u 1 -r 1 -t 10s --headless --only-summary
"""
class UserBehaviour(SequentialTaskSet):
    
    def on_start(self):
        print("Logging In")

    @task
    def flight_finder(self):
        print("Looking for a flight")

    @task
    def select_flight(self):
        print("Selecting a flight")

    @task
    def book_flight(self):
        print("book a flight")

class MyUser(User):
    
    wait_time = between(1, 3)
    host = "www.google.com"
    tasks = [UserBehaviour]
    
    def on_start(self):
        print("Login")
