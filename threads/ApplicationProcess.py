import imp
import threading
import fastapi
import uvicorn
import os
import base64
import logging
import configloader
import json
from database import mysql as db_mysql
import fastapi_router.v0 as v0_router
from tools.base import aes
from tools.base.rsa_utils import openssl as rsa
from fastapi import Response
from fastapi.responses import JSONResponse
class ApplicationProcess(threading.Thread):
    '''
    The FastAPI Process
    '''
    def __init__(self,bind="127.0.0.1",bind_port=8088):
        super().__init__()
        self.bind = "127.0.0.1"
        self.c = configloader.config()
        self.bind_port = bind_port
        self.fastapi = fastapi.FastAPI()
        self.bearer_token = self.c.getkey("bearer_token")
        @self.fastapi.middleware("http")
        async def auth_v0(request: fastapi.Request, call_next):
            request_bearer_token = request.headers.get("Authorization")
            if request_bearer_token is None:
                return JSONResponse(status_code=401,content={"error":"No Authorization header"})
            request_bearer_token = request_bearer_token.replace("Bearer ","")
            if request_bearer_token != self.bearer_token:
                return JSONResponse(status_code=401,content={"error":"Invalid Token"})
            origin_data = await request.body()
            request.state.origin_data = json.loads(origin_data)
            response = await call_next(request)
            return response
        
        self.fastapi.include_router(v0_router.router)
    def run(self):
        uvicorn.run(self.fastapi,host=self.bind,port=self.bind_port)
        uvicorn.main()