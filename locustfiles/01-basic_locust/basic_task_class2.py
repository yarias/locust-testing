from locust import User, TaskSet, task, between

class MyUser(User):
    
    wait_time = between(1, 3)
    host = "www.google.com"
    
    @task
    class UserBehaviour(TaskSet):
        @task
        def add_cart(self):
            print("Add into a cart")
            
        @task
        def view_cart(self):
            print("View Cart")
