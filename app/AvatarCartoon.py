# -*- coding: utf-8 -*-
# Create on 2024/04/30

import base64

from flask import request
from flask import Blueprint

from services.img2img.cute_avatar import create_avatar


app_img2img_create_avatar = Blueprint('app_create_avatar', __name__)
@app_img2img_create_avatar.route('/serving/img2img/AvatarCreate', methods=['POST'])
def _img2img_AvatarCreate(test_reqParams=None):

    if not test_reqParams is None:
        reqParams = test_reqParams
    else:
        reqParams = request.json

    # 参数校验
    user_image = reqParams["image"] if "image" in reqParams and reqParams["image"] else None

    if user_image is None:
        return {"code":-1, "msg":"失败，image 参数为None！", "data":{}}

    # 功能函数调用
    res_dict = create_avatar(Params=reqParams)

    if res_dict.get("flag") != 0:
        return {"code":0, "msg":"失败，{}".format(res_dict.get("msg")), "data":{}}

    else:
        data = {"image": res_dict.get("image")}
        return {"code":0, "msg":"成功！", "data": data}


if __name__ == '__main__':
    from pprint import pprint
    image_path = "../services/img2img/tmp/image.png"

    testParams = {
        "image": base64.b64encode(open(image_path, "rb").read()),
    }


    res_dict = _img2img_AvatarCreate(test_reqParams = testParams)

    pprint(res_dict)
