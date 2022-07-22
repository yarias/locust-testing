from greenlet import GreenletExit
from locust import Locust, seq_task, TaskSequence, between, runners
import sys

sys.path.append("C:\CompleteProjectPart2")
from custom_client_dir.ftp_client import FTPLocust


class UserBehaviour(TaskSequence):

    def on_start(self):
        # Connect to ftp server
        self.my_ftp_connect = self.client.ftp_open_connection()

        # verify if you get welcome message
        if "220 Microsoft" in self.my_ftp_connect.getwelcome():
            ### in case of success -->proceed with login -->else stop locust
            print(self.my_ftp_connect.getwelcome() + "success in connect")
            self.my_login = self.client.ftp_login_server(self.my_ftp_connect, "demo", "password")
            if "User logged in" in self.my_login:
                print(self.my_login + "success in login")
            else:
                runners.locust_runner.quit()

        else:
            runners.locust_runner.quit()

    @seq_task(1)
    def download_file(self):
        file_location = "/pub/example"
        file_name = "readme.txt"
        self.client.ftp_download_file(self.my_ftp_connect, file_location, file_name)
        # verify if file exists at the path

    def on_stop(self):
        self.client.ftp_close_connection(self.my_ftp_connect)
        print("verify goodbye here")


class CustomUser(FTPLocust):
    task_set = UserBehaviour
    wait_time = between(1, 2)
    host = "test1.rebex.net"
