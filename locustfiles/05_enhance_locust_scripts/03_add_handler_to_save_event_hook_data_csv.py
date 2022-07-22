from locust import HttpUser, TaskSet, events, between, task
import socket # imported to print additional info like hostname
import csv

"""
Save event hook data in a CSV file
"""

# To save all stats in a list while executing and at the end save it into a CSV file
request_success_data = [list()] 
request_fail_data = [list()]

# @events.request_success.add_listener # it's the same as in line 24
def on_success_handler(request_type, name, response_time, response_length, **kwargs):
    print("Following request has been completed successfully")
    print(f"Host name: {socket.gethostname()}")
    print(f" type: {request_type}, name: {name}, time: {response_time}, lenght: {response_length}")
    request_success_data.append([socket.gethostname(), request_type, name, response_time, response_length])


# @events.request_failure.add_listener # it's the same as in line 25
def on_failure_handler(request_type, name, response_time, response_length, exception, **kwargs):
    print("Following request has failed")
    print(f" type: {request_type}, name: {name}, time: {response_time}, lenght: {response_length}, exeption: {exception}")
    request_fail_data.append([socket.gethostname(), request_type, name, response_time, response_length, exception])

events.request_success.add_listener(on_success_handler)
events.request_failure.add_listener(on_failure_handler)


def save_success_stats():
    with open("data/success_stats.csv", "w") as f:
        writer = csv.writer(f)
        for value in request_success_data:
            writer.writerow(value)


def save_fail_stats():
    with open("data/fail_stats.csv", "w") as f:
        writer = csv.writer(f)
        for value in request_fail_data:
            writer.writerow(value)

# define a handler that will be executed at the end of the test execution to save stats
def quit_handler(**kwargs):
    save_success_stats()
    save_fail_stats()

# Associate quit_handler with quitting event
events.quitting.add_listener(quit_handler)

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