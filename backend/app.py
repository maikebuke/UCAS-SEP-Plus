
import os
import re
import sys
import ddddocr
from base64 import b64decode
from flask_cors import cross_origin
from flask import Flask, request, Response

ocr = ddddocr.DdddOcr(show_ad=False)

app = Flask(__name__)

@app.before_request
def flask_before_request():
    pass

@app.after_request
def flask_after_request(response: Response):
    sys.stdout.flush()
    return response

@app.route("/", methods=["GET"])
def index():
    return "Hello World!"

JS_BASE64_PATTERN = re.compile(r"^data:[\w\d]+/[\w\d]+;base64,(.+)$")
@app.route("/captcha", methods=["POST"])
@cross_origin()
def handle_captcha():
    # 检查域名是否来自ucas
    assert "ucas.ac.cn" in request.headers.get("Origin")
    # 获取数据
    data = request.get_json()
    assert isinstance(data, dict)
    image_base64 = data.get("image")
    assert re.match(JS_BASE64_PATTERN, image_base64)
    image_base64 = re.findall(JS_BASE64_PATTERN, image_base64)[0]
    image = b64decode(image_base64)
    # ddddocr分类
    captcha_texts = ocr.classification(image)
    resp = {"code": 0, "data": captcha_texts}
    return resp

if __name__ == "__main__":
    app.run("0.0.0.0", "8000", debug=True)
