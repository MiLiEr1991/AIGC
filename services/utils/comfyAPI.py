# 导入所需库
import websocket  # NOTE: 需要安装websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse

import numpy as np


# 定义向服务器发送提示的函数
def queue_prompt(prompt, client_id, server_address):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())


# 定义从服务器下载图像数据的函数
def get_image(server_address, filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()


# 定义获取历史记录的函数
def get_history(server_address, prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())


# 定义通过WebSocket接收消息并下载图像的函数
def get_images(ws, prompt, client_id, server_address):
    prompt_id = queue_prompt(prompt, client_id, server_address)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break  # 执行完成
        else:
            continue  # 预览是二进制数据

    history = get_history(server_address, prompt_id)[prompt_id]
    # print("get_history:",history)
    # print("history_outputs:",history['outputs'])
    # for o in history['outputs']:
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        # print("node_id:",node_id)
        # print("node_output",node_output)
        if 'images' in node_output:
            images_output = []
            for image in node_output['images']:
                print("image:",image)
                image_data = get_image(server_address, image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images


if __name__ == "__main__":

    # 示例JSON字符串，表示要使用的提示
    prompt_text = """
    {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "cfg": 8,
                "denoise": 1,
                "latent_image": [
                    "5",
                    0
                ],
                "model": [
                    "4",
                    0
                ],
                "negative": [
                    "7",
                    0
                ],
                "positive": [
                    "6",
                    0
                ],
                "sampler_name": "euler",
                "scheduler": "normal",
                "seed": 8566257,
                "steps": 20
            }
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": "realvisxlV40_v40LightningBakedvae.safetensors"
            }
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "batch_size": 1,
                "height": 1024,
                "width": 1024
            }
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": [
                    "4",
                    1
                ],
                "text": "masterpiece best quality girl"
            }
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": [
                    "4",
                    1
                ],
                "text": "bad hands"
            }
        },
    "8": {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": [
                "3",
                0
            ],
            "vae": [
                "4",
                2
            ]
        }
    },
    "9": {
        "class_type": "SaveImage",
        "inputs": {
            "filename_prefix": "ComfyUI",
            "images": [
                "8",
                0
            ]
        }
    }
}
"""

    # 将示例JSON字符串解析为Python字典，并根据需要修改其中的文本提示和种子值
    prompt = json.loads(prompt_text)
    prompt["6"]["inputs"]["text"] = "masterpiece best quality man"
    prompt["3"]["inputs"]["seed"] = np.random.randint(0, 999999)

    # 创建一个WebSocket连接到服务器
    server_address = "127.0.0.1:8188"
    client_id = str(uuid.uuid4())

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))

    # 调用get_images()函数来获取图像
    images = get_images(ws, prompt, client_id, server_address)

    # 显示输出图像（这部分已注释掉）
    # Commented out code to display the output images:

# for node_id in images:
#     for image_data in images[node_id]:
#         from PIL import Image
#         import io
#         image = Image.open(io.BytesIO(image_data))
#         image.show()
