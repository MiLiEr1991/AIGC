# -*- coding: utf-8 -*-
# Create on 2024/04/30


from flask import request
from flask import Blueprint

from services.txt2img.create_image import create_image_from_text


app_create_image_from_text = Blueprint('app_create_image_from_text', __name__)
@app_create_image_from_text.route('/serving/txt2img/createImage', methods=['POST'])
def _txt2img_createImage(test_reqParams=None):

    if not test_reqParams is None:
        reqParams = test_reqParams
    else:
        reqParams = request.json

    # 参数校验


    res_dict = create_image_from_text(Params=reqParams)

    data = {}


    return {"code":0, "msg":"成功！", "data":data}


if __name__ == '__main__':
    from pprint import pprint
    test_reqParams = {
    ""
    }

    res_dict = _txt2img_createImage(test_reqParams = test_reqParams)

    pprint(res_dict)
