from dotenv import load_dotenv
load_dotenv()

import queue

from humiolib.HumioClient import HumioIngestClient
import time
import datetime
from faker import Faker
from random import randint
import _thread
import socket
import os
import random

fake = Faker('it_IT')

base_url=os.environ.get("base_url") or "http://13.211.167.47:8080"
ingest_token=os.environ.get("ingest_token") or "03cc2b08-e797-40a2-b635-59e11fc393fc"
print('>>>>>>>>>>>>>>> base_url', base_url)
print('>>>>>>>>>>>>>>> ingest_token', ingest_token)
# client to communicate with humio
client = HumioIngestClient(
    base_url=base_url,
    ingest_token=ingest_token
)



hostname = socket.gethostname()
ipaddress = socket.gethostbyname(hostname)

def log_pi_accesslog():
    # queue logs to avoid missing any
    log_data = queue.Queue()

    def get_new_line(q):
        file = open('/var/log/custom/apache_access.log', 'r')
        while True:
            where = file.tell()
            line = file.readline()
            if not line:
                time.sleep(1)
                file.seek(where)
            else:
                q.put(line)
                

    # start thread to to process syslog's new entries
    _thread.start_new_thread(get_new_line, (log_data,))

    while True:
        # check for new entries and queue then wait for the next
        new_log = log_data.get()
        client.ingest_messages([new_log])

def log_pi_syslog():
    # queue logs to avoid missing any
    log_data = queue.Queue()

    def get_new_line(q):
        # process log you can set syslog.txt to test with
        # file = open('/var/log/custom/apache_access.log', 'r')
        file = open('patterns/syslog')
        lines = file.readlines()
        while True:
            line = lines[int(random.uniform(0, len(lines)-1))]
            q.put(line)
            time.sleep(0.1)
            
    # start thread to to process syslog's new entries
    _thread.start_new_thread(get_new_line, (log_data,))

    while True:
        # check for new entries and queue then wait for the next
        new_log = log_data.get()
        client.ingest_messages([new_log])


def log_pi():
    # queue logs to avoid missing any
    log_access = queue.Queue()
    log_sys = queue.Queue()

    def get_new_line_sys(q):
        # process log you can set syslog.txt to test with
        # file = open('/var/log/custom/apache_access.log', 'r')
        file_syslog = open('patterns/syslog')
        lines_syslog = file_syslog.readlines()
        while True:
            line_syslog = lines_syslog[int(random.uniform(0, len(lines_syslog)-1))]
            q.put(line_syslog)
            time.sleep(1)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', line_syslog)

    def get_new_line_access(q):
        file_accesslog = open('patterns/syslog')         #open('/var/log/custom/apache_access.log', 'r')
        while True:
            where_access = file_accesslog.tell()
            line_access = file_accesslog.readline()
            if not line_access:
                time.sleep(1)
                file_accesslog.seek(where_access)
            else:
                q.put(line_access)
                time.sleep(0.5)
                print(line_access)
            
    # start thread to to process syslog's new entries
    _thread.start_new_thread(get_new_line_sys, (log_sys,))
    _thread.start_new_thread(get_new_line_access, (log_access,))

    while True:
        # check for new entries and queue then wait for the next
        new_log_sys = log_sys.get()
        client.ingest_messages([new_log_sys])

        new_log_access = log_access.get()
        client.ingest_messages([new_log_access])
    

# start thread to log fake new itallians
#_thread.start_new_thread(log_fake_new_clients, ())

# log_pi_accesslog()

# log_pi_syslog()

log_pi()
