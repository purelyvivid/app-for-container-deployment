# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, redirect, url_for, render_template
import os
import socket
import magic
from datetime import datetime

from flask_uploads import UploadSet, configure_uploads, IMAGES,\
 patch_request_class

from predict import predict  #改這行

RESULT_FOLDER = os.path.join('static')

app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()  # 文件储存地址
app.config['UPLOADED_PHOTOS2_DEST'] = os.getcwd()  # 文件储存地址
app.config['RESULT_FOLDER'] = RESULT_FOLDER

photos = UploadSet('photos', IMAGES, default_dest=lambda x: 'photos')
photos2 = UploadSet('photos2', IMAGES, default_dest=lambda x: 'photos2')

configure_uploads(app, [photos, photos2])
patch_request_class(app)  # 文件大小限制，默认为16MB


html = """
    <!DOCTYPE html>
    <title>深度學習圖片風格轉換</title>
    <h1>深度學習圖片風格轉換(tensorflow)</h1>

    <form method=post enctype=multipart/form-data>
    <h2>Upload Image</h2>
         content:<input type=file name=img_file>
         style:<input type=file name=img_file2>
         <input type=submit value=預測>
    </form>
    <hr>
"""

def get_file_url(request):
    """
    當方法是將影像檔直接傳進來
    將傳入的影像檔存在 static/photos 並回傳檔案路徑
    """
    filename = photos.save(request.files['img_file'], folder="static")
    file_url = photos.url(filename)
    return file_url 

def get_file_url2(request):
    """
    當方法是將影像檔直接傳進來
    將傳入的影像檔存在 static/photos2 並回傳檔案路徑
    """
    filename = photos2.save(request.files['img_file2'], folder="static")
    file_url2 = photos2.url(filename)
    return file_url2


def write_result_log(datetime_text, file_url, file_url2, source):
    """
    紀錄每一次的 request
    """
    with open("result_log.csv", "a") as f:
        f.write(f"{datetime_text},{file_url},{file_url2},{source}\n") 

def get_result(request):
    
    # 取得 request 時間字串
    datetime_text = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    
    # 初始值
    file_url, file_url2, result_img_file   = None, None, None
        

    # 將影像檔直接傳進來
    if 'img_file' in request.files and 'img_file2' in request.files:
        file_url = get_file_url(request) #local_file_url 
        file_url2 = get_file_url2(request) #local_file_url

        
        # 取得預測結果
        result_img_file = predict(file_url, file_url2) #改這行

    return datetime_text, file_url, file_url2, result_img_file


@app.route('/', methods=['GET', 'POST'])
def index(): #網頁
    if request.method == 'POST':
        datetime_text, file_url, file_url2, result_img_file  = get_result(request)
        
        result_filename = os.path.join(app.config['RESULT_FOLDER'], 'result.jpg')
        result_img_file.save(result_filename)
        if not result_img_file is None:
            write_result_log(datetime_text, file_url, file_url2, "web_page")
            append_txt = "<br><img width=250 src={}><img width=250 src={}>".format(file_url, file_url2)
            append_txt2 = "<br>結果: <img width=250 src={}>".format(url_for('static', filename='result.jpg'))
            return html + append_txt + append_txt2
    return html




if __name__ == "__main__":
    #app.run('localhost', 5000)
    app.run('0.0.0.0', 5000, debug=True)
