# -*- coding: utf-8 -*-
# Create on 2024/04/30


from flask import request
from flask import Blueprint

from services.ocr.idcard import ocr4idcard

app_ocr = Blueprint('app_ocr', __name__)
@app_ocr.route('/serving/ocr/idcard', methods=['POST'])
def _ocr_idcard(test_reqParams=None):

    if not test_reqParams is None:
        reqParams = test_reqParams
    else:
        reqParams = request.json

    # 参数校验
    image_data = reqParams["imageData"] if "imageData" in reqParams and reqParams["imageData"] else None


    if image_data is None:
        return {"code": -1, "msg": "失败，promptText 参数为None！", "data":{}}

    # 函数调用
    res_dict = ocr4idcard(image_data)

    # 返回结果
    if res_dict.get("flag") != 0:
        return {"code": 0, "msg": "失败，{}".format(res_dict.get("msg")), "data": {}}

    else:
        data = {"image": res_dict.get("data")}
        return {"code": 1, "msg": "成功！", "data": data}


if __name__ == '__main__':
    from pprint import pprint
    image_data = {
    "imageData": "a cute cat."
    }

    res_dict = _ocr_idcard(image_data)

    pprint(res_dict)
