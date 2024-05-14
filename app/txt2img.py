# -*- coding: utf-8 -*-
# Create on 2024/04/30


from flask import request
from flask import Blueprint

from services.txt2img.playground_v25 import create_image

app_create_image_playground = Blueprint('app_create_image_playground', __name__)
@app_create_image_playground.route('/serving/txt2img/playground', methods=['POST'])
def _txt2img_createImage(test_reqParams=None):

    if not test_reqParams is None:
        reqParams = test_reqParams
    else:
        reqParams = request.json

    # 参数校验
    user_txt_prompt = reqParams["promptText"] if "promptText" in reqParams and reqParams["promptText"] else None


    if user_txt_prompt is None:
        return {"code": -1, "msg": "失败，promptText 参数为None！", "data":{}}

    # 函数调用
    res_dict = create_image(Params=reqParams)

    # 返回结果
    if res_dict.get("flag") != 0:
        return {"code": 0, "msg": "失败，{}".format(res_dict.get("msg")), "data": {}}

    else:
        data = {"image": res_dict.get("image")}
        return {"code": 0, "msg": "成功！", "data": data}


if __name__ == '__main__':
    from pprint import pprint
    test_reqParams = {
    "promptText": "a cute cat."
    }

    res_dict = _txt2img_createImage(test_reqParams = test_reqParams)

    pprint(res_dict)
