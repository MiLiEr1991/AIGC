# -*- coding: utf-8 -*-
# Create on 2024/05/17

import base64

from flask import request
from flask import Blueprint

from services.img2img.change_clothes import change_clothes_controlnet

app_change_clothes = Blueprint('app_change_clothes', __name__)
@app_change_clothes.route('/serving/change/clothes', methods=['POST'])
def _change_clothes(test_reqParams=None):

    if not test_reqParams is None:
        reqParams = test_reqParams
    else:
        reqParams = request.json

    # 参数校验
    user_image = reqParams["image"] if "image" in reqParams and reqParams["image"] else None
    prompt_text = reqParams["promptText"] if "promptText" in reqParams and reqParams["promptText"] else None


    if user_image is None:
        return {"code": -1, "msg": "失败，image 参数为None！", "data":{}}

    if prompt_text is None:
        return {"code": -1, "msg": "失败，promptText 参数为None！", "data":{}}

    # 函数调用
    res_dict = change_clothes_controlnet(Params=reqParams)

    # 返回结果
    if res_dict.get("flag") != 0:
        return {"code": 0, "msg": "失败，{}".format(res_dict.get("msg")), "data": {}}

    else:
        data = {"image": res_dict.get("image")}
        return {"code": 0, "msg": "成功！", "data": data}


if __name__ == '__main__':
    from pprint import pprint
    image_path = "../services/img2img/tmp/change_clothes.jpeg"
    test_reqParams = {
    "image": base64.b64encode(open(image_path, "rb").read()),
    "promptText": "blue dress"
    }

    res_dict = _change_clothes(test_reqParams = test_reqParams)

    pprint(res_dict)
