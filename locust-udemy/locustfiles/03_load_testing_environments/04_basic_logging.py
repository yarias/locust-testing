from locust import TaskSet, HttpUser, between, task
import logging

"""
Use logging 

command: locust -f <locust_file.py> --logfile <path__to_save_logs>
"""

logger = logging.getLogger(__name__) # Create a log with the filename

class UserBehaviour(TaskSet):
    
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.user_id = ""
        
    def on_start(self):
        logger.info("Logged into Library Web site")
        with self.client.get("users/1", name="get_user", catch_response=True) as user_resp:
            logger.info(user_resp.text)
            resp = user_resp.json() # Convert JSON response into a dictionary
            if "Bret" in resp["username"]:
                self.user_id = resp["id"]
                user_resp.success()
                logger.info("Request was successful")
            else:
                user_resp.failure("GET Failed")
                logger.critical("Request failed")
        
    @task()
    def add_new_post(self):
        logger.info("Get all the posts by current user")
        with self.client.get(f"posts?userId={self.user_id}", name="add_new_post", catch_response=True) as get_resp:
            last_post_id = get_resp.json()[-1]["id"]
        logger.info("add new post with a concecutive id")
        with self.client.post("posts", name="add_new_post", catch_response=True, data={
            "userId": self.user_id,
            "id": int(last_post_id) + 1,
            "title": "Adding New Post",
            "body": "This is a new post"}
                              ) as post_resp:
            logger.info(post_resp.text)
            if post_resp.status_code == 201:
                post_resp.success()
                logger.info("Request was successful")
            else:
                post_resp.failure("POST Failed")
                logger.critical("Request failed")


    @task()
    def update_comment(self):
        logger.info("Update comment")
        with self.client.put("posts/1", name="update_comment", catch_response=True, data={
            "userId": 1,
            "id": 1,
            "name": "id labore ex et quam laborum",
            "title": "Trying to update",
            "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos"
        }) as put_resp:
            if put_resp.status_code == 201:
                put_resp.success()
                logger.info("Request was successful")
            else:
                put_resp.failure("PUT Failed")
                logger.critical("Request failed")
        logger.info("verify with catch response that select flight is successful")

class MyUser(HttpUser):
    wait_time = between(2, 5)
    host = "https://jsonplaceholder.typicode.com/"
    tasks = [UserBehaviour]