from locust import HttpUser, SequentialTaskSet, task, between


class MySequentialUser(SequentialTaskSet):
    """It is not required to have between and host attributes because the parent class have them"""
    @task
    def post_request(self):
        response = self.client.post("/posts", name="post_new_user", data={"userId": 1000, "id": 1000, "title": "New locust example", "body":"Runninf a POST request from locust"})
        print(response.text)
        print(response.headers)
        print(response.status_code)


    @task
    def get_request(self):
        response = self.client.get("/posts", name="view_posts") # Name used in the report statistics
        print(response.text)
        print(response.headers)
        print(response.status_code)


class MyUser(HttpUser):
    
    wait_time = between(1, 3)
    host= "https://jsonplaceholder.typicode.com"
    tasks = [MySequentialUser] # it automatically calls/executes the task
