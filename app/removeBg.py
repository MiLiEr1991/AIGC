# -*- coding: utf-8 -*-
# Create on 2024/05/17


from flask import request
from flask import Blueprint

from services.removeBg.BRIA import remove_background_bria

app_remove_background_bria = Blueprint('app_remove_background_bria', __name__)
@app_remove_background_bria.route('/serving/removebg/bria', methods=['POST'])
def _removebg_bria(test_reqParams=None):

    if not test_reqParams is None:
        reqParams = test_reqParams
    else:
        reqParams = request.json

    # 参数校验
    user_image = reqParams["image"] if "image" in reqParams and reqParams["image"] else None


    if user_image is None:
        return {"code": -1, "msg": "失败，image 参数为None！", "data":{}}

    # 函数调用
    res_dict = remove_background_bria(Params=reqParams)

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

    res_dict = _removebg_bria(test_reqParams = test_reqParams)

    pprint(res_dict)
