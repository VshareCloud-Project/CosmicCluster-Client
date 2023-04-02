import requests
from tools import request,calculate
import json
import configloader
c = configloader.config()
handler = request.request_handler()
data = {
    "message_id":calculate.genuuid(),
    "message":"test",
    "application":"pvm",
    "destination":calculate.genuuid(),
}

ret = handler.post_request("/v0/east/addmessage",data)
data = {
    "messages":[
        {
            "message_id":calculate.genuuid(),
            "message":"test",
            "application":"pvm",
            "destination":calculate.genuuid(),
        },
        {
            "message_id":calculate.genuuid(),
            "message":"test",
            "application":"pvm",
            "destination":calculate.genuuid(),
        },
        {
            "message_id":calculate.genuuid(),
            "message":"test",
            "application":"pvm",
            "destination":calculate.genuuid(),
        },
        {
            "message_id":calculate.genuuid(),
            "message":"test",
            "application":"pvm",
            "destination":calculate.genuuid(),
        },
        {
            "message_id":calculate.genuuid(),
            "message":"test",
            "application":"pvm",
            "destination":calculate.genuuid(),
        }
    ]
}
ret = handler.post_request("/v0/east/addmessages",data)
print(ret)
new_message_uuid = "2f1bfa0d-12ca-4258-b42a-a5b6ef396b6a"
new_destination_uuid = "e5305c5e-6439-4704-a7d3-3d58e6c3309e"
data = {
    "message_id":new_message_uuid,
    "message":"test",
    "application":"pvm",
    "destination":new_destination_uuid,
}
ret = handler.post_request("/v0/east/getstatus",data)
print(ret)
data = {
    "messages":[
        {
            "message_id":new_message_uuid,
            "message":"test",
            "application":"pvm",
            "destination":new_destination_uuid,
        },
    ]
}
ret = handler.post_request("/v0/east/getmultistatus",data)
print(ret)

data = {
}
ret = handler.post_request("/v0/west/getmessages",data)
print(ret)
messages = ret["messages"]
data = {
    "messages":[]
}
is_first = True
for message_id,message in messages.items():
    if is_first:
        is_first = False
        sign = calculate.sha512(".".join([message_id, c.getkey("client_id"), "pvm", message["message"]]))
        once_data = {
            "message_id":message_id,
            "application":"pvm",
            "sign":sign
        }
        ret = handler.post_request("/v0/west/updatestatus",once_data)
        print(ret)
        continue
    sign = calculate.sha512(".".join([message_id, c.getkey("client_id"), "pvm", message["message"]]))
    data["messages"].append({
        "message_id":message_id,
        "application":"pvm",
        "sign":sign
    })
ret = handler.post_request("/v0/west/updatemultistatus",data)
print(ret)
