from locust import User, between, task, events

"""
test_start and test_stop are evennts that will occour one time before the tests are executed - setup - and when the tests have been executed - teardown -.
They are normal module functions, should not be placed inside the user class, that are decorated with the test_start/stop events, and should have **kwargs as param
When the test_start/stop events are triggered the listener capture them and execute the decorated methods.
"""

@events.test_start.add_listener
def script_start(**kwargs):
    print("Connecting to the DB")


@events.test_stop.add_listener
def script_start(**kwargs):
    print("Disconnecting to the DB")


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
    