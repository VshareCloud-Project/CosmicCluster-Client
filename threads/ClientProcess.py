from threading import Thread, Event
import logging
import requests
from tools import request , status

class ClientProcess(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.event = Event()
        self.has_stopped = False
        self.req = request.request_handler()


    def run(self):
        while True:
            try:
                if self.has_stopped:
                    break
                data = {}
                data["status"] = {
                    "cpu_num": status.get_cpu_cores_num(),
                    "cpu_persent":status.get_cpu(),
                    "uptime":status.get_uptime(),
                    "memory_total":status.get_memory()[0],
                    "memory_used":status.get_memory()[1],
                    "hdd_all_total":status.get_hdd()[0],
                    "hdd_all_used":status.get_hdd()[1],
                    "disk_info":status.get_disk_info()
                }
                data["tasks"] = {
                    #TODO: "taskid":Task Content
                }

                res = self.req.post_request("/v0/gettask",data)
                logging.info("Update System status Successful.")
                if res["ret"] != 0:
                    logging.error(res["msg"])
                
            except:
                import traceback
                logging.error(traceback.format_exc())
            self.event.wait(120)
            

    def stop(self):
        self.has_stopped = True
        self.event.set()