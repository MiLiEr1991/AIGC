import io
import json
import os
import base64

import random
import numpy as np

from paddleocr import PaddleOCR

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

ocr = PaddleOCR(
    text_detection_model_name="PP-OCRv5_mobile_det",
    text_detection_model_dir="./models/PP-OCRv5_mobile_det",
    text_recognition_model_name="./models/PP-OCRv5_mobile_rec",
    text_recognition_model_dir="./models/PP-OCRv5_mobile_rec",
    textline_orientation_model_name="PP-LCNet_x1_0_textline_ori",
    textline_orientation_model_dir="./models/PP-LCNet_x1_0_textline_ori",
    use_doc_orientation_classify=False, # Disables document orientation classification model via this parameter
    use_doc_unwarping=False, # Disables text image rectification model via this parameter
    use_textline_orientation=True, # Disables text line orientation classification model via this parameter
)


def base64ToImage(image_base64, save_path):
    # 解码图片
    imgdata = base64.b64decode(image_base64)
    # 将图片保存为文件
    with open(save_path, 'wb') as f:
        f.write(imgdata)



def ocr4idcard(img_path=None, img_base64=None):

    res_dict = dict()

    try:
        result = ocr.predict(img_path)

        if result:
            res_dict['flag'] = 0
            res_dict['msg'] = "成功！"
            res_dict['data'] = result

        else:
            res_dict['flag'] = 1
            res_dict['msg'] = "失败！"
            res_dict['data'] = []


    except Exception as err:
        res_dict['flag'] = 1
        res_dict['msg'] = f"失败, {str(err)}!"
        res_dict['data'] = []

    return res_dict




if __name__ == "__main__":
    from pprint import pprint
    from PIL import Image
    image_path = "./tmp/image.png"
    # pic_base64 = base64.b64encode(open(image_path, "rb").read())
    res = ocr4idcard(img_path=image_path)
    if res.get("flag") != 0:
        print("faild!")

    pprint(res)