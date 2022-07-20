from asyncio import tasks
from multiprocessing import Event
from locust import User, TaskSet, between, task

import locust.event # Import event module where EventHook class is defined

"""
Create and use custom EventHooks

EventHooks will be listenning to a particular condition and be associated with particular handlers or logics that will be executed when these 
events are fired. Locust fires built-in events in different classes for particular cases

event occurs:
    EventHook -> handlers -> action 

cliente.py:
    fire response related events
    request_success & request_failure
    
runner.py:
    fire and handle hatching related events
    Also fire & handle events for erros and quit

Steps:
    1. Create an instace of the EventHook class
    2. Create event_handler/function that will be executed when the event hook is fired
    3. Associate the event_handler/functions to the EventHook instance created using `.add_listerner()`
    
    Note: All these is defined at module level
"""

custom_event_hook = locust.event.EventHook() # Creante an EventHook
custom_event_hook2 = locust.event.EventHook() # Creante an EventHook

# 2. Create handlers to execute whent he eventHook is triggered
# **kwargs as a parameter to avoid errors, so that in case any extra argument passed to the handler while firing the event cannot cause any error.
def handler_add(a, b, **kwargs): 
    print(f"add: {a + b}")

def handler_diff(a, b, **kwargs):
    print(f"diff: {a - b}")

# 3. Associate event hook with handlers
custom_event_hook.add_listener(handler_add)
custom_event_hook2.add_listener(handler_diff)


class UserBehaviour(TaskSet):
    @task
    def my_task(self):
        print("Inside my task")
        flag = True
        if flag is True:
            custom_event_hook.fire(a=1, b=3, mgs="I am done")
        else:
            custom_event_hook2.fire(a=1, b=3, mgs="I am done")


class MyUser(User):
    wait_time = between(2, 5)
    tasks = [UserBehaviour]
    host = "https://www.google.com"