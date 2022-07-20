from locust import TaskSet, HttpUser, between, task
from locust.exception import StopUser

"""
Exit/Stop an user when the step fails --> raise StopUser 
Stop test execution (runner) --> self.environment.runner.quit()
"""

class UserBehaviour(TaskSet):
    def on_start(self):
        with self.client.get("/", name="GetRoot", catch_response=True) as response:
            if "google" in response.text:
                response.success()
            else:
                response.failure("Failed to get root")
                self.parent.environment.runner.quit() # Exit test run


    @task
    def search_url(self):
        with self.client.get("/search?q=python", name="SearchPython", catch_response=True) as resp:
            if "Python" in resp.text:
                resp.success()
            else:
                resp.failure("Failed serching for Python")
                raise StopUser() # Exit User


class MyUser(HttpUser):
    wait_time = between(2, 5)
    host = "https://www.google.com"
    tasks = [UserBehaviour]