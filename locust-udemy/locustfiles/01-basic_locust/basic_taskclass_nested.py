from locust import User, TaskSet, task, between

"""
Issue with nested TaskSet: MyUser is executed which executes UserBehaviour which has nested classes, but it gets sticked with one of the nested classes
and cannot take tasks from the other one unless it is interrupted.
"""
class UserBehaviour(TaskSet):

    @task
    class CartModule(TaskSet):

        @task
        def add_cart(self):
            print("Add cart")


        @task
        def delete_cart(self):
            print("Delete cart")

    @task
    class ProductModule(TaskSet):
        @task
        def view_product(self):
            print("View product")

        @task
        def add_product(self):
            print("Add product")

class MyUser(User):
    
    wait_time = between(1, 3)
    host = "www.google.com"
    tasks = [UserBehaviour]
