from fastapi import APIRouter, Request, Response, BackgroundTasks
import json
import importlib
from fastapi.responses import JSONResponse
from database import mysql as db_mysql
import time
import base64
import datetime
from database import session_helper,redis_queue
from tools import calculate

router = APIRouter(prefix="/v0",
                   responses={
                       404: {
                           "ret": 404,
                           "msg": "Not found"
                       },
                       500: {
                           "ret": 500,
                           "msg": "Server error"
                       },
                       400: {
                           "ret": 400,
                           "msg": "Bad request"
                       },
                       401: {
                           "ret": 401,
                           "msg": "UnAuthorized"
                       }
                   })


@router.post("/ping")
async def post_ping(request: Request):
    return JSONResponse({"ret": 0, "msg": "pong"})

@router.post("/status")
async def post_status(request: Request):
    data = request.state.origin_data
    taskid = data["taskid"]
    #TODO: Check the response is ready

    return JSONResponse({"ret": 0, "msg": "pong"})

@router.post("/addtask")
async def post_addtask(request: Request):
    data = request.state.origin_data
    application = data["application"]
    app_function = data["app_function"]
    appdata = data["appdata"]

    task = {
        "application": application,
        "app_function": app_function,
        "appdata": appdata,
        "method":"addtask"
    }
    task["taskid"] = calculate.generate_uuid()
    task["status"] = "waiting"
    task["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    redis_queue.RedisQueue("task").push(task)
    return JSONResponse({"ret": 0, "msg": "OK","taskid":task["taskid"]})

@router.post("/updatetask")
async def post_updatetask(request: Request):
    data = request.state.origin_data
    taskid = data["taskid"]
    application = data["application"]
    app_function = data["app_function"]
    appdata = data["appdata"]
    task_status = data["status"]
    task = session_helper.Session("done_task").get("task"+taskid)
    if task is not None:
        return JSONResponse({"ret": 1, "msg": "Task is done"})
    task = {
        "application": application,
        "app_function": app_function,
        "appdata": appdata,
        "taskid":taskid,
        "method":"updatetask",
        "status":task_status,
        "origin_task":session_helper.Session("task").get("task"+taskid)
    }
    task["taskid"] = calculate.generate_uuid()
    task["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    redis_queue.RedisQueue("task").push(task)
    return JSONResponse({"ret": 0, "msg": "OK","taskid":task["taskid"]})

@router.post("/check")
async def post_check(request: Request):
    data = request.state.origin_data
    taskid = data["taskid"]
    task = session_helper.Session("done_task").get("taskid"+taskid)
    if task is None:
        return JSONResponse({"ret": 1, "msg": "Task is not done"})
    return JSONResponse({"ret": 0, "msg": "OK","task":task})