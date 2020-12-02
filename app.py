from os import access
from dotenv import load_dotenv
load_dotenv()

import queue
import datetime
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

def log_pi():
    # queue logs to avoid missing any
    access_log_q = queue.Queue()
    sys_log_q = queue.Queue()

    def get_new_line_sys(q):
        # process log you can set syslog.txt to test with
        file = open('patterns/syslog')
        lines = file.readlines()
        length = len(lines)
        while True:
            line = lines[int(random.uniform(0, length-1))]
            q.put(line)
            

    def get_new_line_access(q):
         # process log you can set accesslog.txt to test with
        file = open('patterns/accesslog')
        lines = file.readlines()
        lenght = len(lines)
        while True:
            line = lines[int(random.uniform(0, lenght-1))]
            q.put(line)
            
    # start thread to to process syslog's new entries
    _thread.start_new_thread(get_new_line_sys, (sys_log_q,))
    _thread.start_new_thread(get_new_line_access, (access_log_q,))

    while True:
        # check for new entries and queue then wait for the next
        new_log_sys = sys_log_q.get()
        new_cur_sys = changeToCurrentTime(new_log_sys, 'sys')
        #print('>>>>syslog', new_cur_sys)
        client.ingest_messages([new_log_sys])

        new_log_access = access_log_q.get()
        new_cur_access = changeToCurrentTime(new_log_access, 'access')
        #print('>>>>accesslog', new_cur_access)
        client.ingest_messages([new_log_access])

        time.sleep(0.01)
    

def changeToCurrentTime(strOld, mode):
    if mode == 'access':
        substr = strOld[strOld.find('[')+1 : strOld.find('[')+21]
        return strOld.replace(substr, getCurrentTime(mode)) 
    elif mode == 'sys':
        substr = strOld[ : 15]
        return strOld.replace(substr, getCurrentTime(mode))


def getCurrentTime(mode): 
    if mode == 'access':
        today = datetime.datetime.today().strftime("%d/%b/%Y")   
        now = datetime.datetime.now().strftime("%H:%M:%S")
        return ( today + ':' + now )
    elif mode == 'sys':
        today = datetime.datetime.today().strftime("%b %d")   
        now = datetime.datetime.now().strftime("%H:%M:%S")
        return ( today + ' ' + now )


log_pi()



