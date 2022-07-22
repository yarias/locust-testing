from locust import TaskSet, User, task, between

"""
Define user behaviors with a group of tasks
"""

class UserBehaviour(TaskSet):
    @task
    def add_to_cart(self):
        print("Adding into a cart")

    @task
    def view_product(self):
        print("View a product")


class MyUser(User):
    
    wait_time = between(1, 3)
    host = "www.google.com"
    tasks = [UserBehaviour]
    
    def on_start(self):
        print("Login")
