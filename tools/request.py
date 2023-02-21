import os
import sys
import requests
import base64
import json
if __name__ == "__main__":
    import inspect
    file_path = os.path.dirname(
        os.path.realpath(
            inspect.getfile(
                inspect.currentframe())))
    sys.path.insert(0, os.path.join(file_path, '../'))
import configloader
from tools.base import aes,rsa_utils

class request_handler:
    def __init__(self) -> None:
        self.c = configloader.config()
        self.url = self.c.getkey("server_endpoint")
        self.public_key_filename = self.c.getkey("rsa_public_key")
        fp = open(self.public_key_filename,"rb")
        self.public_key = fp.read()
        fp.close()
        self.private_key_filename = self.c.getkey("rsa_private_key")
        fp = open(self.private_key_filename,"rb")
        self.private_key = fp.read()
        fp.close()
        self.server_public_key_filename = self.c.getkey("server_public_key")
        fp = open(self.server_public_key_filename,"rb")
        self.server_public_key = fp.read()
        fp.close()
        self.client_id = self.c.getkey("client_id")
        self.client_cipher = rsa_utils.rsa_utils(self.public_key,self.private_key)
        self.server_cipher = rsa_utils.rsa_utils(self.server_public_key)
    def post_request(self,path,data):
        data = json.dumps(data)
        req_data = {
            "user_id": self.client_id,
        }
        newpasswd = aes.genpassword(32)
        req_data["encrypt"] = aes.cbc_encrypt(data.encode(),newpasswd)
        req_data["sign"] = base64.b64encode(self.client_cipher.sign(req_data["encrypt"].encode())).decode()
        req_data["token"] = base64.b64encode(self.server_cipher.encrypt(newpasswd.encode())).decode()
        req_data["token_sign"] = base64.b64encode(self.client_cipher.sign(req_data["token"].encode())).decode()
        req_data = json.dumps(req_data)
        url = self.url + path
        r = requests.post(url,data=req_data)
        if r.status_code != 200:
            raise Exception("Request failed")
        need_decrypt = r.json()
        encrypted_data = need_decrypt["encrypt"]
        encrypted_token = base64.b64decode(need_decrypt["token"])
        encrypted_sign = base64.b64decode(need_decrypt["sign"])
        encrypted_token_sign = base64.b64decode(need_decrypt["token_sign"])
        encrypted_token_decrypt1 = self.client_cipher.decrypt(encrypted_token)
        assert self.server_cipher.verify(encrypted_data.encode(),encrypted_sign) == True
        assert self.server_cipher.verify(need_decrypt["token"].encode(),encrypted_token_sign) == True
        encrypted_data_decrypt = aes.cbc_decrypt(encrypted_data,encrypted_token_decrypt1.decode())
        return json.loads(encrypted_data_decrypt)

if __name__ == "__main__":
    r = request_handler()
    data = r.post_request("/v0/ping",{})
    print(data)