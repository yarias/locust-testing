from locust import User, between

"""
Tasks as attributes: we define module functions that will receive a class as a parameter and inside the UserClass 
we define the tasks attribute with a list of the methods we'll define as tasks
"""


def add_to_cart(userclass):
    print("Adding into a cart")


def view_product(userclass):
    print("View a product")


class MyUser(User):
    
    wait_time = between(1, 3)
    host = "www.google.com"
    # tasks = [add_to_cart, view_product]
    tasks = {add_to_cart:2, view_product:6} # to define a weightage
    
    def on_start(self):
        print("Login")
        
