# Locust Documentation
http://docs.locust.io/en/stable/index.html

## Commnand Line:
Locust version: `locust -v`
Locust web interface: http://localhost:8089 

### Run a locustfiles.py test located in same path 
`locust` (automatically looks for locustfile.py)

# Locust User class
Represents one user. Locust will spawn one instance of the User for each user is being simulated. There are some attributes that the User calss may define:

### await_time attribute
Used to introduce delays after each task execution
* `constant` for a fixed amount of time
* `between` for a ramdom time between a min and max value
* `constant_throughput` for an adaptive time that nsures the task runs (at most) X times per second
* `constant_pacing` for an adptive time that ensures the task runs (at most) once every X seconds

It is possblre to add your own `wait_time` method directly on your class.
For example, the following User class would sleep for one second, then two, then three, etc.
```
class MyUser(User):
    last_wait_time = 0

    def wait_time(self):
        self.last_wait_time += 1
        return self.last_wait_time
```

### weight and fixed_count attributes
If more than one user class exists in the file, and no user classes are specified on the command line, Locust will spawn an equal number of each of the user classes.

You can specify which user classes to use: `locust -f locust_file.py WebUser MobileUser`

* `weight`: increase/decrease the probability to simulate more users of certain class
```
class WebUser(User):
    weight = 3 # 3 times more likely than MobileUser
    ...

class MobileUser(User):
    weight = 1
    ...
```
* `fixed_count`: the weight property will be ignored and the exact count users will be spawned.
```
class AdminUser(User):
    wait_time = constant(600)
    fixed_count = 1
```

### host attrubute
It is a URL prefix to the host that will be loaded. It can be specified in de command line with `--host` option, or in the web UI.
If one declares the host attrbute in the user class, it will be used in case no `--host` is specified in the command line or web UI.

### task attribute
A user class can have tasks declared as methods under it using the `@task` decorator, but one can also specify tasks using `tasks` attribute

* `@task decorator` is the easiest way to add a task for a User. It takes an optional weight argument that ca be used to specify the task's execution ration.
```
class MyUser(User):
    wait_time = between(5, 15)

    @task(3)
    def task1(self):
        pass

    @task(6)
    def task2(self):
        pass
```
* `task attribute` is either a list of Tasks or a <Task: int>. dictionary, where Task is either a python callable or a TaskSet class. If the task is a normal python function they receive a single argument which is the User instance that is executing the task.
```
from locust import User, constant

def my_task(user):
    pass

class MyUser(User):
    tasks = [my_task]
    wait_time = constant(1)
```
If the tasks attribute is specified as a list, each time a task is to be performed, it will be randomly chosen from the tasks attribute. If however, tasks is a dict, the task that is to be executed will be chosen at random but with the int as ratio. So with a task that looks like this: `{my_task: 3, another_task: 1}` may_task would be 3 time more likely to be executed than another_task. Internally, the dict is expanded into a list: `[my_task, my_task, my_task, another_task]`
* `@tag_decorator` used to decorate `@tasks`, then you can select what tasks are executed during the test using `--tags` and `--exclude-tags` arguments, for example, `--tags tag1` (execute tasks 1&2) or `--exclute-tags tag1` (executes task 1)
from locust import User, constant, task, tag
```
class MyUser(User):
    wait_time = constant(1)

    @tag('tag1')
    @task
    def task1(self):
        pass

    @tag('tag1', 'tag2')
    @task
    def task2(self):
        pass

    @task
    def task3(self):
        pass
```

### environment attribute
A reference to the `environment` in which the user is running. Use this to interact with the environment, or the `runner` which it contains.
Stop runner from a task method: `self.environment.runner.quit()`

### on_start and on_stop methods
Users (and TaskSets) can declare an `on_start` method and/or `on_stop` method. A user will call its `on_start` method when it starts running, and its `on_stop` when it stops running.

### Events hooks

* `test_start` and `test_stop`
If you need to run some code at the start or stop of a load test, you should use the `test_start` and `test_stop` events. You can setup listeners for these events at the module level of your locustfile:
```
from locust import events

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("A new test is starting")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("A new test is ending")
```
* `init`
The `init` event is triggered at the beginning of each Locust process. This is especially useful in distributed mode where each worker process (not each user) needs a chance to do some initialization. For example, let’s say you have some global state that all users spawned from this process will need:
```
from locust import events
from locust.runners import MasterRunner

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        print("I'm on master node")
    else:
        print("I'm on a worker or standalone node")
```
    * Using `init` we can also add web end-points to the web UI. we can retrieve a reference to the Flask app instance and use that to set up a new route
    ```
    from locust import events

    @events.init.add_listener
    def on_locust_init(environment, **kw):
        @environment.web_ui.app.route("/added_page")
        def my_added_page():
            return "Another page"
        ```
* `init_command_line_parser` used to add custom command line argument
```
@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--my-argument", type=str, env_var="LOCUST_MY_ARGUMENT", default="", help="It's working")
    # Set `include_in_web_ui` to False if you want to hide from the web UI
    parser.add_argument("--my-ui-invisible-argument", include_in_web_ui=False, default="I am invisible")
``` 
* `request` set up an event listener that will trigger after a request is completed. (**kwargs) it prevents the code from breaking if new arguments are added in some future version of Locust
```
from locust import events

@events.request.add_listener
def my_request_handler(request_type, name, response_time, response_length, response,
                       context, exception, start_time, url, **kwargs):
    if exception:
        print(f"Request to {name} failed with exception {exception}")
    else:
        print(f"Successfully made a request to: {name})
        print(f"The response was {response.text}")
```

## HttpUser class
It is the most commonly used User. It adds a `client` attribute which is used to make HTTP requests (`self.client.get("/")`). 

* `client` is an instance of `HttpSession`. `HttpSession` is a subclass/wrapper for `requests.Session`. Just like requests.Session, it preserves cookies between requests so it can easily be used to log in to websites.
* Validating responses: Requests are considered successful if the HTTP response code is OK (<400), but you can do additional validations, like mark a request as failed by using the `catch_response` argument, a `with-statement` and a call to `response.failure()`
```
with self.client.get("/", catch_response=True) as response:
    if response.text != "Success":
        response.failure("Got wrong response")
    elif response.elapsed.total_seconds() > 0.5:
        response.failure("Request took too long") # response.success() is the opposite
```
You can even avoid logging a request at all by throwing an exception and then catching it outside the with-block. Or you can throw a locust exception, like in the example below, and let Locust catch it.
```
from locust.exception import RescheduleTask
...
with self.client.get("/does_not_exist/", catch_response=True) as response:
    if response.status_code == 404:
        raise RescheduleTask() # if the request failed we avoid to log it and reschedule the task
```
* Grouping requests
Group URLs that contain dynamic parameter together in User's statistics.
    * Using the `name` argument:  
    ```
    # Statistics for these requests will be grouped under: /blog/?id=[id]
    for i in range(10):
        self.client.get("/blog?id=%i" % i, name="/blog?id=[id]")
    ```
    * setting the `client.request_name` attribute
    ```
    self.client.request_name="/blog?id=[id]"
    for i in range(10):
        self.client.get("/blog?id=%i" % i)
    self.client.request_name=None
    ```
    * chain multiole grouping using `client.rename_request()` context manager
    ```
    @task
    def multiple_groupings_example(self):

        # Statistics for these requests will be grouped under: /blog/?id=[id]
        with self.client.rename_request("/blog?id=[id]"):
            for i in range(10):
                self.client.get("/blog?id=%i" % i)

        # Statistics for these requests will be grouped under: /article/?id=[id]
        with self.client.rename_request("/article?id=[id]"):
            for i in range(10):
                self.client.get("/article?id=%i" % i)
    ```

## Distributed load generation
To start a master you use the `--master` flag and `--worker` flag, but if the worker wont be running on the same machine; then you use `--master-host` to point out to the Host/IP of the machine running the master.

The master instance runs Locust’s web interface, and tells the workers when to spawn/stop Users. The workers run your Users and send back statistics to the master. The master instance doesn’t run any Users itself.

Both the master and worker machines must have a copy of the locustfile when running Locust distributed.

`locust -f my_locustfile.py --worker --master-host=192.168.0.14`

Example:
`master`: run `locust -f my_locustfile.py --master` if we want to wait until the expected number of worker is running `--expected-workers=<#>`
`worker_1`: run `locust -f my_locustfile.py --worker` if master is in another host then provide `--master-host <IP>` and `--master-port <port>` as well
`worker_2`: run `locust -f my_locustfile.py --worker`

Running in AWS
Create the instances 
Install Python -> create an env
Install locust
Go to security groups and allow connection between master and workers (IP/Ports)


## Running without the web UI
for example if you want to run it in some automated flow, like a CI server - by using the `--headless` flag together with -u and -r

If you want to specify the run time for a test, you can do that with `--run-time` or `-t`
By default, locust will stop your tasks immediately (without even waiting for requests to finish). If you want to allow your tasks to finish their iteration, you can use `--stop-timeout <seconds>`:

`locust -f --headless -u 1000 -r 100 --run-time 1h30m --stop-timeout 99`

Running Locus distributed, you should specify the `--expect-workers` option when starting the master node

To control the exit code for a Locust process, for example, when running Locust in a CI environment.

```
import logging
from locust import events

@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 0.01:
        logging.error("Test failed due to failure ratio > 1%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 200:
        logging.error("Test failed due to average response time ratio > 200 ms")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 800:
        logging.error("Test failed due to 95th percentile response time > 800 ms")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0
```
## Retrieve test statistics in CSV format

There are two ways to consume stats in CSV files. 
First, when running Locust with the web UI, you can retrieve CSV files under the Download Data tab.
Secondly, you can run Locust with a flag which will periodically save three CSV files. This is particularly useful if you plan on running Locust in an automated way with the --headless flag:

`locust -f examples/basic.py --csv=example --headless -t10m`

The files will be named `example_stats.csv`, `example_failures.csv` and `example_history.csv` (when using `--csv=example`).

## Docker with Locust

Docker and AWS EC2 instance:

* Install Docker on the VM
* Add ec2_user in docker group (`sudo usermod -aG docker ec2_user`) if not you must use sudo before each docker command
* Pull locust image or proide one
* docker run -p 8089:8089 -v <path/to/container/data/>:*/mnt/locust* locust/locust -f */mnt/locust*/locustfile.py

docker-compose up <service-name>
docker-compose config (to check if the file is fine
dockercompose scale <service-name=#>