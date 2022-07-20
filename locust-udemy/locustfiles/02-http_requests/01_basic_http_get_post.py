from locust import HttpUser, task, between

class MyUser(HttpUser):
    
    wait_time = between(1, 3)
    host= "https://jsonplaceholder.typicode.com"
        
    @task
    def get_request(self):
        self.client.get("/posts", name="view_posts") # Name used in the report statistics
        
    @task
    def post_request(self):
        self.client.post("/posts", name="post_new_user", data={"userId": 1000, "id": 1000, "title": "New locust example", "body":"Runninf a POST request from locust"})
