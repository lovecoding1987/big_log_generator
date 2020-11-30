import queue

from humiolib.HumioClient import HumioIngestClient
import time
import datetime
import os
from faker import Faker
from random import randint
import _thread
import socket

fake = Faker('it_IT')

# client to communicate with humio
client = HumioIngestClient(
    base_url="http://13.211.167.47:8080",
    ingest_token="03cc2b08-e797-40a2-b635-59e11fc393fc")

hostname = socket.gethostname()
ipaddress = socket.gethostbyname(hostname)

def log_pi_syslog():
    # log raspberry pi syslog

    # queue logs to avoid missing any
    log_data = queue.Queue()

    def get_new_line(q):
        # process log you can set syslog.txt to test with
        print('>>> Open /var/log/syslog .......')
        file = open('/var/log/syslog', 'r')
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
        print(new_log)
        client.ingest_messages([f'{ipaddress} - {new_log}'])


def log_fake_new_clients():
    # log fake new itallian clients by generating random names
    while True:
        # print(f'{str(datetime.datetime.utcnow())} : New Client {fake.name()}')
        client.ingest_messages([f'{ipaddress} - {str(datetime.datetime.utcnow())} : New fake message {fake.text()}'])
        #time.sleep(randint(1, 5))
        time.sleep(0.001)
    

# start thread to log fake new itallians
_thread.start_new_thread(log_fake_new_clients, ())

log_pi_syslog()
