from locust import task, User, between

class MyUser(User):
    
    wait_time = between(1, 3)
    host = "www.google.com"
    
    def on_start(self):
        print("Login")
        
    @task(2) # Give a task a weight
    def add_to_cart(self):
        print("Adding into a cart")

    @task(4)
    def view_product(self):
        print("View a product")
