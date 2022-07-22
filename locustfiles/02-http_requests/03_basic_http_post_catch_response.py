from locust import HttpUser, SequentialTaskSet, task, between

"""
Use "with" context along with the "catch_response" argument to handle the response and make validations
Use <response>.success() or <response>.failure() to set the step pass or fail.
"""

class MySequentialUser(SequentialTaskSet):
    """It is not required to have between and host attributes because the parent class have them"""
    @task
    def post_request(self):
        with self.client.post("/posts", name="post_new_user",
                              data={"userId": 1000, "id": 1000, "title": "New locust example", "body":"Runninf a POST request from locust"},
                              catch_response=True) as post_resp:
            # print(f"post response: {post_resp.text}")
            if "New locust example" in post_resp.text:
                post_resp.success()
            else:
                post_resp.failure("Failed to psot date")

    @task
    def get_request(self):
        with self.client.get("/posts", name="view_posts", catch_response=True) as get_response:
            # print(f"get response: {get_response.text}")
            if "delectus eligend" in get_response.text:
                get_response.success()
            else:
                get_response.failure("Failed to get data")


class MyUser(HttpUser):
    
    wait_time = between(1, 3)
    host= "https://jsonplaceholder.typicode.com"
    tasks = [MySequentialUser] # it automatically calls/executes the task
