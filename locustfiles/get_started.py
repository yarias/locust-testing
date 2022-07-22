from locust import HttpUser, task

# Get Started
class HelloWorldUser(HttpUser):
    host="https://google.com"
    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")
