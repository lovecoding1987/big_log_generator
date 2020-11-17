import queue

from humiolib.HumioClient import HumioIngestClient
import time
import datetime
import os
from faker import Faker
from random import randint
import _thread

fake = Faker('it_IT')

# client to communicate with humio
client = HumioIngestClient(
    base_url="http://54.252.31.50:8080",
    ingest_token="a1a539c8-c808-49fa-9721-b1cc3fc3503f")


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
    try:
        print('Trying start get_new_line thread')
        _thread.start_new_thread(get_new_line, (log_data,))
    except:
        print ("Error: unable to start thread")

    while 1:
        pass

    while True:
        # check for new entries and queue then wait for the next
        new_log = log_data.get()
        print(new_log)
        client.ingest_messages([new_log])


def log_fake_new_clients():
    # log fake new itallian clients by generating random names
    while True:
        #print(f'{str(datetime.datetime.utcnow())} : New Client {fake.name()}')
        client.ingest_messages([f'{str(datetime.datetime.utcnow())} : New Client {fake.name()}'])
        #time.sleep(randint(1, 5))
        time.sleep(0.001)
    

# start thread to log fake new itallians
try:
   _thread.start_new_thread(log_fake_new_clients, ())
except:
   print ("Error: unable to start thread")

while 1:
   pass


log_pi_syslog()
