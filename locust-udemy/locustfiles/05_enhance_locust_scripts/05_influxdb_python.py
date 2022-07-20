from locust import HttpLocust, TaskSet, task, between, events
from influxdb import InfluxDBClient
import json
import socket
import datetime
import pytz

host=socket.gethostname()
client=InfluxDBClient(host="localhost",port="8086")
client.switch_database("DemoDB_Locust2")

def individual_success_handle(request_type,name,response_time,response_length,**kwargs):
    print(request_type+ name+str(response_time)+str(response_length))
    SUCCESS_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s","status":"%s"' \
                       '},"time":"%s","fields": {"responseTime": "%s","responseLength":"%s"}' \
                       '}]'
    json_string=SUCCESS_TEMPLATE%("ResponseTable",host,name,request_type,"OK",datetime.datetime.now(tz=pytz.UTC),response_time,response_length)
    print(json_string)
    client.write_points(json.loads(json_string))

def individual_fail_handle(request_type,name,response_time,response_length,exception,**kwargs):
    FAIL_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s","exception":"%s","status":"%s"' \
                    '},"time":"%s","fields": {"responseTime": "%s","responseLength":"%s"}' \
                    '}]'
    json_string=FAIL_TEMPLATE%("ResponseTable",host,name,request_type,exception,"FAIL",datetime.datetime.now(tz=pytz.UTC),response_time,response_length)
    print(json_string)
    client.write_points(json.loads(json_string))

events.request_success+=individual_success_handle
events.request_failure+=individual_fail_handle

class UserBehaviour(TaskSet):
    @task(1)
    def profile(self):
        self.client.get("/breweries")


class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    wait_time = between(5, 9)
    host = "https://api.openbrewerydb.org"