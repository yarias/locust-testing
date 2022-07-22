###Assignment
# Connect to FTP server
# Login to FTP server
# Change to desired directory
# Retrieve File
# Disconnect FTP Server
###Assignment--Solution

from locust import Locust
from ftplib import FTP

import sys

sys.path.append("C:\CompleteProjectPart2")

from utility.time_measure import decorate_time


class SampleFTPClient:

    def __init__(self, host):
        self.host = host

#open FTP connection
    @decorate_time
    def ftp_open_connection(self):
        ftp_connect = FTP(self.host)
        return ftp_connect

#login to FTP server
    @decorate_time
    def ftp_login_server(self, ftp_connect, username, password):
        ftp_login = ftp_connect.login(username, password)
        return ftp_login

#Change to directory & retrieve file in binary format
    @decorate_time
    def ftp_download_file(self, ftp_connect, file_location, file_name):
        ftp_connect.cwd(file_location)
        local_file = open(file_name, 'wb')
        ftp_connect.retrbinary('RETR ' + file_name, local_file.write, 1024)
        local_file.close()

##Method place holder to upload file
    @decorate_time
    def ftp_upload_file(self):
        pass

##Close FTP connection
    @decorate_time
    def ftp_close_connection(self, ftp_connect):
        ftp_connect.quit


class FTPLocust(Locust):

    def __init__(self, *args, **kwargs):
        super(FTPLocust, self).__init__(*args, **kwargs)
        self.client = SampleFTPClient(self.host)
