from locust import HttpUser, TaskSet, events, between, task
import locust.event
import socket # imported to print additional info like hostname

"""
Create 2 handlers and associate them with request_success and request_failure
Handler must print individual request data to console and add some aditional info pertaining to request
"""

# @events.request_success.add_listener # it's the same as in line 24
def on_success_handler(request_type, name, response_time, response_length, **kwargs):
    print("Following request has been completed successfully")
    print(f"Host name: {socket.gethostbyname()}")
    print(f" type: {request_type}, name: {name}, time: {response_time}, lenght: {response_length}")


# @events.request_failure.add_listener # it's the same as in line 25
def on_failure_handler(request_type, name, response_time, response_length, exception, **kwargs):
    print("Following request has failed")
    print(f" type: {request_type}, name: {name}, time: {response_time}, lenght: {response_length}, exeption: {exception}")


events.request_success.add_listener(on_success_handler)
events.request_failure.add_listener(on_failure_handler)


class UseBehaviour(TaskSet):
    @task
    def searh(self):
        with self.client.get("/asdasd", name="serach_google", catch_response=True) as resp:
            if resp.status_code == "200":
                print("request was successful, there should be a comment from the success event hook")
            else:
                print("request failed, there should be a comment from the fail event hook")

class MyUser(HttpUser):
    wait_time = between(2, 5)
    host = "https://www.google.com"
    tasks = [UseBehaviour]