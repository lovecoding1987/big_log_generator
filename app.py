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

def log_pi_syslog():
    # log raspberry pi syslog

    # queue logs to avoid missing any
    log_data = queue.Queue()

    def get_new_line(q):
        # process log you can set syslog.txt to test with
        print('>>> Open /var/log/custom/apache_access.log .......')
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
        #print(new_log)
        client.ingest_messages([new_log])


def log_fake_new_clients():
    # log fake new itallian clients by generating random names
    while True:
        # print(f'{str(datetime.datetime.utcnow())} : New Client {fake.name()}')
        client.ingest_messages([f'{ipaddress} - {str(datetime.datetime.utcnow())} : New fake message {fake.text()}'])
        #time.sleep(randint(1, 5))
        time.sleep(0.1)
    

# start thread to log fake new itallians
#_thread.start_new_thread(log_fake_new_clients, ())

log_pi_syslog()
