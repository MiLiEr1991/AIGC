import os
os.environ.setdefault("PADDLE_PDX_LOCAL_FONT_FILE_PATH", "./fonts/simfang.ttf")

from paddleocr import PaddleOCR  

ocr = PaddleOCR(
    text_detection_model_dir="./models/PP-OCRv5_server_det",
    text_recognition_model_dir="./models/PP-OCRv5_server_rec",
    use_doc_orientation_classify=False, # Disables document orientation classification model via this parameter
    use_doc_unwarping=False, # Disables text image rectification model via this parameter
    use_textline_orientation=True, # Disables text line orientation classification model via this parameter
)

test_img_root = "data/imgs2"
img_file_list = [item for item in os.listdir(test_img_root) if item.endswith(".jpeg")]
for img_file in img_file_list:
    img_path = os.path.join(test_img_root, img_file)

    result = ocr.predict(img_path)
    for res in result:
        # res.print()
        save_path = "output/test2-2"
        res.save_to_img("output/test2-2")
        res.save_to_json("outputtest2-2")

