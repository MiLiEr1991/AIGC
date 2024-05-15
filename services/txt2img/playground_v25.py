# -*- coding: utf-8 -*-
# Create on 2024/04/30
import io
import os
import json
import uuid
import base64

import sys
# 获取当前文件所在的目录路径, 将当前文件目录添加到sys.path，以便可以导入该目录下的模块
sys.path.append(os.path.dirname(os.path.realpath((__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


import numpy as np

from PIL import Image
from copy import deepcopy
from services.utils.comfyAPI import get_images
from services.utils.gpt import gpt_zhipu

import websocket  # NOTE: 需要安装websocket-client (https://github.com/websocket-client/websocket-client)



BASE_DIR = os.path.dirname(os.path.realpath(__file__))

default_neg_prompt = """ugly, deformed, noisy, blurry, distorted, out of focus, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, missing fingers,"""

with open(os.path.join(BASE_DIR, './workflows/workflow_api_playground_v25.json'), 'rb') as f:
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

    prompt_update['1']['inputs']['text'] = prompt_dict.get("pos_prompt")
    prompt_update['2']['inputs']['text'] = prompt_dict.get("neg_prompt")
    prompt_update['5']['inputs']['seed'] = np.random.randint(0, 999999)
    prompt_update['12']['inputs']['value'] = prompt_dict.get("width")
    prompt_update['13']['inputs']['value'] = prompt_dict.get("height")

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
            res_dict['image'] = images.get('7')[0]

        else:
            res_dict['flag'] = 1
            res_dict['msg'] = "失败, comfy返回为空！"
            res_dict['image'] = []


    except Exception as err:
        res_dict['flag'] = 1
        res_dict['msg'] = "失败, {}!".format(str(err))
        res_dict['image'] = []

    return res_dict





def create_image(Params):

    user_txt_prompt = Params["promptText"]
    user_txt_neg_prompt = Params["negPromptText"] if "negPromptText" in Params and Params["negPromptText"] else default_neg_prompt
    user_img_prompt = Params["promptImage"] if "promptImage" in Params and Params["promptImage"] else None
    image_size = Params["imageSize"] if "imageSize" in Params and Params["imageSize"] else [1024, 1024]
    client_id = Params["clientId"] if "clientId" in Params and Params["clientId"] else str(uuid.uuid4())
    server_url = Params["serverUrl"] if "serverUrl" in Params and Params["serverUrl"] else "127.0.0.1:8188"
    use_gpt = Params["useGpt"] if "useGpt" in Params and Params["useGpt"] else True

    if not use_gpt:
        update_txt_prompt = user_txt_prompt
    else:
        update_txt_prompt = gpt_zhipu(user_txt_prompt)


    prompt_dict = dict()
    prompt_dict["pos_prompt"] = update_txt_prompt
    prompt_dict["neg_prompt"] = user_txt_neg_prompt
    prompt_dict["seed"] = np.random.randint(0, 9999999)
    prompt_dict["width"] = image_size[0]
    prompt_dict["height"] = image_size[1]

    prompt_update = load_comfy_workflow(default_workflow, prompt_dict)

    seg_dict = comfy_api(client_id, server_address=server_url, prompt=prompt_update)

    if seg_dict.get('flag') == 0:
        seg_dict['image'] = base64.b64encode(seg_dict.get('image')).decode()

    return seg_dict



if __name__ == '__main__':
    from pprint import pprint
    test_reqParams = {
    "promptText": "a cute cat",
    "imageSize": [768, 1024]
    }

    res = create_image(Params = test_reqParams)
    if res.get("flag") != 0:
        print("faild!")
    else:
        image_base64 = base64.b64decode(res['image'])
        Image.open(io.BytesIO(image_base64)).show()
        print("end")

        pprint(res)