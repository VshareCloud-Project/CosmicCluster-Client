import requests
import json
data = {
    "application": "test",
    "app_function": "test",
    "appdata": "test"
}
headers = {
    "Content-Type": "application/json",
    "Authorization":"Bearer 1145141919810",
}
r = requests.post("http://127.0.0.1:8001/v0/addtask", data=json.dumps(data), headers=headers)
print(r.text)