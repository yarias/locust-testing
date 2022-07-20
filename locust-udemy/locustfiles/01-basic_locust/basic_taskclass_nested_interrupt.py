from locust import User, TaskSet, task, between

"""
Issue with nested TaskSet: MyUser is executed which executes UserBehaviour which has nested classes, but it gets sticked with one of the nested classes
and cannot take tasks from the other one unless it is interrupted.
"""
class UserBehaviour(TaskSet):

    @task(2)
    class CartModule(TaskSet):

        @task(4)
        def add_cart(self):
            print("Add cart")

        @task(2)
        def delete_cart(self):
            print("Delete cart")

        @task(1)
        def stop(self):
            print("stop cart")
            self.interrupt() # interrupt the taskSet and gives control back to the parent taskSet. If reschedule=True the parent User will immediately re-schedule, and execute, a new task.

    @task(4)
    class ProductModule(TaskSet):
        @task(4)
        def view_product(self):
            print("View product")

        @task(2)
        def add_product(self):
            print("Add product")
        
        @task(1)
        def stop(self):
            print("stop product")
            self.interrupt()

class MyUser(User):
    
    wait_time = between(1, 3)
    host = "www.google.com"
    tasks = [UserBehaviour]
