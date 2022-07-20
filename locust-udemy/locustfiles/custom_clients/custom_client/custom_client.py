from locust import User
from locustfiles.custom_clients.Utilities.time_measure import decorate_time


class SampleCustomClient:
    
    def __init__(self, host) -> None:
        self.host = host 

    @decorate_time
    def custom_req_conn(self):
        print("Perform your connection")

    @decorate_time
    def custom_send_conn(self):
        print("Perform your send request here!")

    @decorate_time
    def custom_req_discnn(self):
        print("Perform your diconnection")
        

class CustomLocust(User):
    
    def __init__(self, *args, **kwargs):
        super(CustomLocust, self).__init__(*args, **kwargs)
        self.client = SampleCustomClient(self.host)