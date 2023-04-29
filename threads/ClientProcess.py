from threading import Thread, Event
import logging
import requests
from tools import request , status , calculate
from database import session_helper,redis_queue
import configloader

app_messages_verify = session_helper.Session("app_messages_verify") #APP验证的消息
app_messages_to_server = session_helper.Session("app_messages_to_server") #APP发给服务端的消息
server_messages_verify = session_helper.Session("server_messages_verify") #服务端验证的消息
server_messages_to_app = session_helper.Session("server_messages_to_app") #服务端发给APP的消息

class ClientProcess(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.event = Event()
        self.has_stopped = False
        self.req = request.request_handler()
        self.queue = redis_queue.RedisQueue("task")
        self.session = session_helper.Session("task")
        self.done_session = session_helper.Session("done_task")
        self.c = configloader.config()
        self.client_id = self.c.getkey("client_id")


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
                data["west"] = {}
                data["east"] = {}
                res = self.req.post_request("/gettask",data)
                west_data = res["west"]
                for i in west_data:
                    sign = west_data[i]["sign"]
                    app = west_data[i]["application"]
                    message = server_messages_verify.get(".".join([app, i]))
                    if message == None:
                        continue
                    if calculate.sha512_verify(
                        ".".join([i, self.client_id, app, message]), sign):
                        server_messages_verify.remove(".".join([self.client_id, app, i]))
                east_data = res["east"]
                for i in east_data:
                    destination = east_data[i]["destination"]
                    message = east_data[i]["message"]
                    app = east_data[i]["application"]
                
            except:
                import traceback
                logging.error(traceback.format_exc())
            self.event.wait(120)
            

    def stop(self):
        self.has_stopped = True
        self.event.set()