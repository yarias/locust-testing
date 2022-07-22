from locust import User, task, between

"""cmd: locust -f locustfiles/basic_multi_user_weightage.py <UserClass> to select what user client to simulate or none for all available
"""

class WebUser(User):
    weight = 3
    wait_time=between(1, 5)
    host="www.google.com"
    
    @task
    def get_root(self):
        print("WebUser")


class MobileUser(User):
    weight = 1
    wait_time=between(1, 5)
    host="www.google.com"
    
    @task
    def get_root(self):
        print("MobileUser")
