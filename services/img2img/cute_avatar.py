# -*- coding: utf-8 -*-
# Create on 2024/05/16
import io
import os
import json
import uuid
import base64

import sys
# 获取当前文件所在的目录路径, 将当前文件目录添加到sys.path，以便可以导入该目录下的模块
sys.path.append(os.path.dirname(os.path.realpath((__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from copy import deepcopy
from services.utils.comfyAPI import get_images
from services.segment.SAM import segment_anything
import websocket  # NOTE: 需要安装websocket-client (https://github.com/websocket-client/websocket-client)


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, './workflows/workflow_api_create_avatar_dream_controlnet.json'), 'rb') as f:
    content = f.read()
    default_workflow_A = json.loads(content)
    
with open(os.path.join(BASE_DIR, './workflows/workflow_api_create_avatar_dream_controlnet_instantid.json'), 'rb') as f:
    content = f.read()
    default_workflow_B = json.loads(content)

def base64ToImage(image_base64, save_path):
    # 解码图片
    imgdata = base64.b64decode(image_base64)
    # 将图片保存为文件
    with open(save_path, 'wb') as f:
        f.write(imgdata)


def load_comfy_workflow(workflow_json, prompt_dict):

    # 加载工作流
    if isinstance(workflow_json, dict):
        prompt_default = workflow_json
    else:
        prompt_default = json.loads(workflow_json)

    prompt_update = deepcopy(prompt_default)

    prompt_update['1']['inputs']['image'] = prompt_dict.get("image_path")

    return prompt_update


def comfy_api(client_id, server_address, prompt):
    res_dict = dict()

    try:
        # 创建一个WebSocket连接到服务器
        server_address = server_address

        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))

        # 调用get_images()函数来获取图像
        images = get_images(ws, prompt, client_id, server_address)

        if images:
            res_dict['flag'] = 0
            res_dict['msg'] = "成功！"
            res_dict['image'] = images.get('87')[0]

        else:
            res_dict['flag'] = 1
            res_dict['msg'] = "失败, comfy返回为空！"
            res_dict['image'] = []


    except Exception as err:
        res_dict['flag'] = 1
        res_dict['msg'] = "失败, {}!".format(str(err))
        res_dict['image'] = []

    return res_dict



def create_avatar(Params):

    client_id = Params["clientId"] if "clientId" in Params and Params["clientId"] else str(uuid.uuid4())
    input_image_base64 = Params["image"]
    server_url = Params["serverUrl"] if "serverUrl" in Params and Params["serverUrl"] else "127.0.0.1:8188"
    avatar_type= Params["avatar_type"] if "avatar_type" in Params and Params["avatar_type"] else "0"
    # 缓存图片
    tmp_image_path = os.path.join(BASE_DIR, "./tmp/", str(uuid.uuid4())+".jpg")
    base64ToImage(input_image_base64, save_path=tmp_image_path)

    prompt_dict = dict()
    prompt_dict["image_path"] = tmp_image_path
    if avatar_type=="0":
        prompt_update = load_comfy_workflow(default_workflow_A, prompt_dict)
    else:
        prompt_update = load_comfy_workflow(default_workflow_B, prompt_dict)


    res_comfy = comfy_api(client_id, server_address=server_url, prompt=prompt_update)

    if res_comfy.get('flag') == 0:
        res_comfy['image'] = base64.b64encode(res_comfy.get('image')).decode()

    return res_comfy


if __name__ == "__main__":
    from pprint import pprint
    from PIL import Image

    image_path = f"{BASE_DIR}/tmp/yaoming.png"
    testParams = {
        "image": base64.b64encode(open(image_path, "rb").read()),
        "avatar_type":"1"
    }

    res = create_avatar(Params=testParams)
    if res.get("flag") != 0:
        print("faild!")
    else:
        image_base64 = base64.b64decode(res['image'])
        Image.open(io.BytesIO(image_base64)).save(image_path.replace(".png", "_avatar.jpg"))

    pprint(res)