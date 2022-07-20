from multiprocessing.spawn import import_main_path
import time
from locust import HttpUser, task, between

# For a file to be a valid locustfile it must contain at least one class inheriting from 'User'.
class QuickUser(HttpUser):
    '''
    This class defines the user we'll be simulating. It inherits from 'HttpUser' which gives each user a client attribute,
    that can be used to make HTTP requests to the target system. 
    
    When a test starts, locust will create an instance of this class for every user that it simulates, and each of these
    users will start running within their own green g-event thread.

    '''
    # make the simulated users wait between 1 and 5 seconds after each task is executed
    wait_time = between(1, 5)
    
    @task # For every running user, Locust creates a greenlet (micro-thread), that will call all methods decorated with @tasks.
    def hello_world(self):
        self.client.get('/hello') # makes it possible to make HTTP calls that will be logged by Locust
        self.client.get('/world')

    # Tasks are picked at randomly, but you can give them different weighting. It will make Locust three times more likely to pick view_items than hello_world
    @task(3)
    def view_items(self):
        for id in range(10):
            # since the stats is grouped on the URL - we use the name parameter to group all those requests under an entry named "/item" instead.
            self.client.get(f"/item?id={id}", name="/item")
            time.sleep(1)

    # A method with this name will be called for each simulated user when they start.
    def on_start(self):
        self.client.post("/login", json={"username":"foo", "password":"bar"})
