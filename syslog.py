from dotenv import load_dotenv
load_dotenv()

import queue
from humiolib.HumioClient import HumioIngestClient
import time
import _thread
import os
import random
from common import changeToCurrentTime

base_url=os.environ.get("base_url")
ingest_token=os.environ.get("syslog_token")

client = HumioIngestClient(
    base_url=base_url,
    ingest_token=ingest_token
)


def log_pi():
    sys_log_q = queue.Queue()

    def get_new_line_sys(q):
        file = open('patterns/syslog')
        lines = file.readlines()
        length = len(lines)
        while True:
            line = lines[int(random.uniform(0, length-1))]
            q.put(line)
            

    _thread.start_new_thread(get_new_line_sys, (sys_log_q,))
    
    while True:
        new_log_sys = sys_log_q.get()
        new_cur_sys = changeToCurrentTime(new_log_sys, 'sys')
        #print('>>>>syslog', new_cur_sys)
        client.ingest_messages([new_cur_sys])        

        time.sleep(0.01)

log_pi()



