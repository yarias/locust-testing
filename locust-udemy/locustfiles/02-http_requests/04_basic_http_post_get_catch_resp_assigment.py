from locust import HttpUser,SequentialTaskSet,task,between

USER_ID = None # Instead of using glabla variable it can be substitute with a __init__ and setting a self.user_id = None in UserBehaviour class

class UserBehaviour(SequentialTaskSet):

    def on_start(self):
        global USER_ID
        # Commenting below as the page does not exist, bit keeping it as reference of login POST request
        # with self.client.post("/login.php", name="login", data={"action": "process","userName": "qamile1@gmail.com",
        #                                                    "password": "qamile","login.x": "41","login.y": "12"}, catch_response=True) as resp:

        #     if ("Find a Flight") in resp.text:
        #         resp.success()
        #     else:
        #         resp.failure("failed to login")
        print("Logged into Library Web site")
        with self.client.get("users/1", name="get_user", catch_response=True) as user_resp:
            print(user_resp.text)
            resp = user_resp.json() # Convert JSON response into a dictionary
            if "Bret" in resp["username"]:
                USER_ID = resp["id"]
                user_resp.success()
            else:
                user_resp.failure("GET Failed")
        
    @task()
    def add_new_post(self):
        print("Get all the posts by current user")
        with self.client.get(f"posts?userId={USER_ID}", name="add_new_post", catch_response=True) as get_resp:
            last_post_id = get_resp.json()[-1]["id"]
        print("add new post with a concecutive id")
        with self.client.post("posts", name="add_new_post", catch_response=True, data={
            "userId": USER_ID,
            "id": int(last_post_id) + 1,
            "title": "Adding New Post",
            "body": "This is a new post"}
                              ) as post_resp:
            print(post_resp.text)
            if post_resp.status_code == 201:
                post_resp.success()
            else:
                post_resp.failure("POST Failed")


    @task()
    def update_comment(self):
        print("Update comment")
        with self.client.put("posts/1", name="update_comment", catch_response=True, data={
            "userId": 1,
            "id": 1,
            "name": "id labore ex et quam laborum",
            "title": "Trying to update",
            "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos"
        }) as put_resp:
            if put_resp.status_code == 201:
                put_resp.success()
            else:
                put_resp.failure("PUT Failed")
        print("verify with catch response that select flight is successful")


class MyUser(HttpUser):
    wait_time=between(1,2)
    host="https://jsonplaceholder.typicode.com/"
    tasks=[UserBehaviour]
