# -*- coding: utf-8 -*-

from flask import Flask


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


_ctx = app.app_context()
_ctx.push()

from app.ocr import app_ocr
app.register_blueprint(app_ocr)


if __name__== '__main__':
    import sys
    port = 80
    if len(sys.argv) == 2:
        port = sys.argv[1]
    app.run(host='0.0.0.0', port=port, debug=False)