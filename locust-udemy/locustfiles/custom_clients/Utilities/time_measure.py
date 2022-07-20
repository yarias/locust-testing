from unittest import expectedFailure
from locust import events
import time
import sys


def decorate_time(func):
    
    def wrapper(*args, **kwargs):
        task_name = sys._getframe(1).f_code.co_name
        start_time = time.time()
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            total_time = int(time.time() - start_time) * 1000
            events.request_failure.fire(request_type="custom_req", name=task_name, response_time=total_time, response_length="", exception=e)
        else:
            total_time = int(time.time() - start_time) * 1000
            events.request_success.fire(request_type="custom_req", name=task_name, response_time=total_time, response_length="")
        return result
    
    return wrapper