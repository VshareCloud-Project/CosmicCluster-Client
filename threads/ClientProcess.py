from threading import Thread, Event
import logging
import requests
from tools import request , status
from database import session_helper,redis_queue

class ClientProcess(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.event = Event()
        self.has_stopped = False
        self.req = request.request_handler()
        self.queue = redis_queue.RedisQueue("task")
        self.session = session_helper.Session("task")
        self.done_session = session_helper.Session("done_task")


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
                data["check"] = []
                check_list = self.session.find("check")
                for check in check_list:
                    data["check"].append(self.session.get("check"+check))
                data["tasks"] = {
                    
                }
                while not self.queue.empty():
                    task = self.queue.pop()
                    data["tasks"][task["taskid"]] = task
                    self.session.add("task"+task["taskid"],task)
                res = self.req.post_request("/v0/gettask",data)
                for i in check_list:
                    if i not in data["check"]:
                        # The mission is missing, should be add it to the queue.
                        self.queue.push(self.session.get("taskid"+i))
                        self.session.remove("taskid"+i)
                    else:
                        # check the status of the mission
                        if data["check"][i]["status"] == "done":
                            # The mission is done, should be remove it from the queue.
                            self.session.remove("taskid"+i)
                            self.done_session.add("taskid"+i,data["taskid"][i],86400)
                        else:
                            # The mission is not done, should be update the information.
                            self.session.add("taskid"+i,data["taskid"][i])
                            
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