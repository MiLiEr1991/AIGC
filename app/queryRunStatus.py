# -*- coding: utf-8 -*-
# Create on 2024/04/30
import os
import base64

from flask import request
from flask import Blueprint

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


app_query_running_status = Blueprint('app_query_running_status', __name__)
@app_query_running_status.route('/serving/query/runstatus', methods=['POST'])
def _query_running_status(test_reqParams=None):

    if not test_reqParams is None:
        reqParams = test_reqParams
    else:
        reqParams = request.json

    # 参数校验
    task = reqParams["task"] if "task" in reqParams and reqParams["task"] else None
    client_id = reqParams["clientId"] if "clientId" in reqParams and reqParams["clientId"] else None

    if task is None:
        return {"code":-1, "msg":"失败，task 参数为None！", "data":{}}

    if client_id is None:
        return {"code":-1, "msg":"失败，clientId 参数为None！", "data":{}}

    # 功能函数调用
    file_path = os.path.join(BASE_DIR.replace("app", ""), "./services/res/", "{}_{}.png".format(task, str(client_id)))

    if not os.path.exists(file_path):
        return {"code":1, "msg":"未完成!", "data":{}}

    else:
        data = {"image": base64.b64encode(open(file_path, "rb").read()).decode()}
        return {"code":0, "msg":"已完成！", "data": data}


if __name__ == '__main__':
    from pprint import pprint

    testParams = {
        "task": "txt2img",
        "clientId": "ad2a9070-ad22-4868-a341-c08380d4b9f0",
    }


    res_dict = _query_running_status(test_reqParams = testParams)

    pprint(res_dict)
