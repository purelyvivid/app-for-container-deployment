# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, redirect, url_for
import os
import socket
import magic
from datetime import datetime

from flask_uploads import UploadSet, configure_uploads, IMAGES,\
 patch_request_class

from loadimg import load_img_rgb #改這行
from predict import predict  #改這行


app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()  # 文件储存地址

photos = UploadSet('photos', IMAGES, default_dest=lambda x: 'photos')
configure_uploads(app, photos)
patch_request_class(app)  # 文件大小限制，默认为16MB

html = '''
    <!DOCTYPE html>
    <title>深度學習影像分類</title>
    <h1>mobilenet_v2 深度學習影像分類(pytorch)</h1>
    <h2>Upload Image</h2>
    <form method=post enctype=multipart/form-data>
         <input type=file name=img_file>
         <input type=submit value=預測>
    </form>
    <h2>From Image URL</h2>
    <form method=post enctype=multipart/form-data>
         URL:<input type=text name=img_file_pth>
         <input type=submit value=預測>
    </form>
    <hr>
    '''

def get_file_url(request):
    """
    當方法是將影像檔直接傳進來
    將傳入的影像檔存在 static/photos 並回傳檔案路徑
    """
    filename = photos.save(request.files['img_file'], folder="static", name="")
    file_url = photos.url(filename)
    return file_url 

def write_result_log(datetime_text, file_url, result_txt, method, source):
    """
    紀錄每一次的 request
    """
    with open("result_log.csv", "a") as f:
        f.write(f"{datetime_text},{file_url},{result_txt},{method},{source}\n") 

def get_result(request):
    
    # 取得 request 時間字串
    datetime_text = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    
    # 初始值
    file_url, result_txt, method  = None, None, "No class"
        
    # 將影像檔的路徑傳進來
    if ('img_file_pth' in request.form) and (request.form['img_file_pth']!=""):
        method = 'img_load_from_path'
        file_url = request.form['img_file_pth'] # remote_file_url
        print(file_url)
        input_imgarr = load_img_rgb(file_url) 

    # 將影像檔直接傳進來
    elif 'img_file' in request.files:
        method = 'img_file'
        file_url = get_file_url(request) #local_file_url  
        input_imgarr = load_img_rgb(file_url) 
    
    # 取得預測結果
    result_txt = predict(input_imgarr) #改這行

    return datetime_text, file_url, result_txt, method


@app.route('/', methods=['GET', 'POST'])
def index(): #網頁
    if request.method == 'POST':
        datetime_text, file_url, result_txt, method = get_result(request)
        if not file_url is None:
            write_result_log(datetime_text, file_url, result_txt, method, "web_page")
            return html + '<br><img width=250 src=' + file_url + '>' + '<br>預測結果: <B>' + result_txt + '</B>'
    return html

if __name__ == "__main__":
    #app.run('localhost', 5000)
    app.run('0.0.0.0', 5000, debug=True)
