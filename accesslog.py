from dotenv import load_dotenv
load_dotenv()

import queue
from humiolib.HumioClient import HumioIngestClient
import time
from random import randint
import _thread
import os
import random
from common import changeToCurrentTime

base_url=os.environ.get("base_url")
ingest_token=os.environ.get("accesslog_token")

client = HumioIngestClient(
    base_url=base_url,
    ingest_token=ingest_token
)


def log_pi():
    access_log_q = queue.Queue()
            

    def get_new_line_access(q):
        file = open('/opt/dummydata/patterns/accesslog')
        lines = file.readlines()
        lenght = len(lines)
        while True:
            linenumber = int(random.uniform(0, lenght-1))
            line = lines[linenumber]
            q.put(line)
            time.sleep(0.01)
            
    _thread.start_new_thread(get_new_line_access, (access_log_q,))

    while True:
    
        new_log_access = access_log_q.get()
        new_cur_access = changeToCurrentTime(new_log_access, 'access')
        #print('>>>>accesslog', new_cur_access)
        client.ingest_messages([new_cur_access])


log_pi()



