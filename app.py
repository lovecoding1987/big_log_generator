from dotenv import load_dotenv
load_dotenv()

import queue
from humiolib.HumioClient import HumioIngestClient
import time
from random import randint
import _thread
import os
from random import uniform, randint
from common import changeToCurrentTime

base_url=os.environ.get("base_url")

accesslog_client = HumioIngestClient(
    base_url=base_url,
    ingest_token=os.environ.get("accesslog_token")
)
syslog_client = HumioIngestClient(
    base_url=base_url,
    ingest_token=os.environ.get("syslog_token")
)

accesslog_q = queue.Queue()
syslog_q = queue.Queue()
        

def get_new_line_accesslog(q):
    file = open('/opt/dummydata/patterns/accesslog')
    lines = file.readlines()
    length = len(lines)
    while True:
        linenumber = randint(0, length-1)
        line = lines[linenumber]
        q.put(line)
        time.sleep(uniform(0.01, 0.05))

def get_new_line_syslog(q):
    file = open('/opt/dummydata/patterns/syslog')
    lines = file.readlines()
    length = len(lines)
    while True:
        linenumber = randint(0, length-1)
        line = lines[linenumber]
        q.put(line)
        time.sleep(uniform(0.01, 0.05))
        
#_thread.start_new_thread(get_new_line_syslog, (syslog_q,))

def send_accesslog(q):
    while True:    
        new_log_access = q.get()
        new_cur_access = changeToCurrentTime(new_log_access, 'access')
        #print('>>>>>>>>>>>>', new_cur_access)
        accesslog_client.ingest_messages([new_cur_access])

def send_syslog(q):
    while True:    
        new_log_sys = q.get()
        new_cur_sys = changeToCurrentTime(new_log_sys, 'sys')
        #print('============', new_cur_sys)
        syslog_client.ingest_messages([new_cur_sys])

try:
    _thread.start_new_thread(get_new_line_accesslog, (accesslog_q,)) 
    _thread.start_new_thread(get_new_line_syslog, (syslog_q,)) 
    
    _thread.start_new_thread(send_accesslog, (accesslog_q, ))   
    _thread.start_new_thread(send_syslog, (syslog_q, ))           
except:
    print("Error: unable to start thread")

while 1:
    pass