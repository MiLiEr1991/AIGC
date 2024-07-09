# -*- coding: utf-8 -*-

from flask import Flask


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


_ctx = app.app_context()
_ctx.push()

from app.txt2img import app_create_image_playground
app.register_blueprint(app_create_image_playground)

from app.lamaRemover import app_img2img_lama_remover
app.register_blueprint(app_img2img_lama_remover)

# 查运行状态
from app.queryRunStatus import app_query_running_status
app.register_blueprint(app_query_running_status)

if __name__== '__main__':
    import sys
    port = 80
    if len(sys.argv) == 2:
        port = sys.argv[1]
    app.run(host='0.0.0.0', port=port, debug=False)