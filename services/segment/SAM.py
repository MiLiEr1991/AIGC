import io
import json
import os
import base64

import random
import websocket  # NOTE: 需要安装websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import numpy as np
from copy import deepcopy
from services.utils.comfyAPI import get_images


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(BASE_DIR, './workflows/workflow_api_sam.json'), 'rb') as f:
    content = f.read()
    default_workflow = json.loads(content)


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
            res_dict['image'] = images

        else:
            res_dict['flag'] = 1
            res_dict['msg'] = "失败, comfy返回为空！"
            res_dict['image'] = []


    except Exception as err:
        res_dict['flag'] = 1
        res_dict['msg'] = "失败, {}!".format(str(err))
        res_dict['image'] = []

    return res_dict



def segment_anything(client_id, input_image_base64, user_workflow, server_url="127.0.0.1:8188"):


    # 缓存图片
    tmp_image_path = os.path.join(BASE_DIR, "./tmp/", str(uuid.uuid4())+".jpg")
    base64ToImage(input_image_base64, save_path=tmp_image_path)

    if user_workflow:
        workflow = user_workflow
    else:
        workflow = default_workflow

    prompt_dict = dict()
    prompt_dict["image_path"] = tmp_image_path

    prompt_update = load_comfy_workflow(workflow, prompt_dict)

    seg_dict = comfy_api(client_id, server_address=server_url, prompt=prompt_update)

    return seg_dict


if __name__ == "__main__":
    from pprint import pprint
    from PIL import Image
    image_path = "./tmp/image.png"
    pic_base64 = base64.b64encode(open(image_path, "rb").read())
    client_id = str(uuid.uuid4())
    res = segment_anything(client_id=client_id, input_image_base64=pic_base64, user_workflow=None)
    if res.get("flag") != 0:
        print("faild!")
    else:
        image_base64 = res['image'].get("4")[0]
        Image.open(io.BytesIO(image_base64)).save(image_path.replace(".png", "_seg.jpg"))

    pprint(res)