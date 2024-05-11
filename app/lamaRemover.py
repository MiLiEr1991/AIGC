# -*- coding: utf-8 -*-
# Create on 2024/04/30

import base64
from flask import request
from flask import Blueprint

from services.img2img.inpaint_lama import inpaint_image_with_lama


app_img2img_lama_remover = Blueprint('app_lama_remover', __name__)
@app_img2img_lama_remover.route('/serving/img2img/lamaRemover', methods=['POST'])
def _img2img_lamaRemover(test_reqParams=None):

    if not test_reqParams is None:
        reqParams = test_reqParams
    else:
        reqParams = request.json

    # 参数校验
    user_image = reqParams["image"] if "image" in reqParams and reqParams["image"] else None
    area_bbox = reqParams["bbox"] if "bbox" in reqParams and reqParams["bbox"] else None
    area_mask = reqParams["mask"] if "mask" in reqParams and reqParams["mask"] else None

    if user_image is None:
        return {"code":-1, "msg":"失败，image 参数为None！", "data":{}}

    if area_bbox is None and area_mask is None:
        return {"code":-1, "msg":"失败，bbox 和 mask 参数不得同时为None！", "data":{}}

    # 功能函数调用
    res_dict = inpaint_image_with_lama(Params=reqParams)

    if res_dict.get("flag") != 0:
        return {"code":0, "msg":"失败，{}".format(res_dict.get("msg")), "data":{}}

    else:
        data = res_dict.get("data")
        return {"code":0, "msg":"成功！", "data":data}


if __name__ == '__main__':
    from pprint import pprint
    image_path = "../services/img2img/tmp/image.png"
    mask_path = "../services/img2img/tmp/mask.png"
    testParams = {
        "image": base64.b64encode(open(image_path, "rb").read()),
        "mask": base64.b64encode(open(mask_path, "rb").read()),
    }

    res_dict = _img2img_lamaRemover(test_reqParams = testParams)

    pprint(res_dict)
