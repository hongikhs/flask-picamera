# 라즈베리파이 원격 카메라
# 웹브라우저를 통해 라즈베리파이 카메라 사용

import picamera         # 라즈베리파이 카메라 모듈
import datetime         # 현재 날짜와 시간을 알려주는 모듈
from flask import Flask # 웹서버 구현을 위한 모듈

app = Flask(__name__)   # 웹서버 초기화
f = ''                  # 사진 및 동영상 파일 이름 기억을 위한 변수
cam = ''                # 카메라 객체를 위한 변수
html = ''               # 촬영목록 html 태그 저장을 위한 변수
html_still = '<a href="./still"><button>사진 촬영</button></a> '    # 사진촬영 버튼 html 태그
html_record = '<a href="./record"><button>녹화 시작</button></a> '  # 동영상녹화 버튼 html 태그
html_stop = '<a href="./stop"><button>녹화 종료</button></a> '      # 동영상정지 버튼 html 태그

@app.route('/')         # 웹브라우저가 http://주소/를 요청할 때 실행할 함수
def home():
    global html_still, html_record, html
    return html_still + html_record + html

@app.route('/still')    # 웹브라우저가 http://주소/still을 요청할 때 실행할 함수
def still():
    global f, html_still, html_record, html
    f = str(datetime.datetime.now()) + '.jpg' # 현재 날짜와 시간으로 파일 이름 생성
    cam = picamera.PiCamera()
    cam.start_preview()
    cam.capture('./static/' + f)
    cam.stop_preview()
    cam.close()
    html = '<br><a href="/static/' + f + '">' + f + '</a>' + html
    return html_still + html_record + html

@app.route('/record')    # 웹브라우저가 http://주소/record를 요청할 때 실행할 함수
def record():
    global f, html_stop, html, cam
    f = str(datetime.datetime.now()) + '.h264'
    cam = picamera.PiCamera()
    cam.start_preview()
    cam.start_recording('./static/' + f)
    return html_stop + html

@app.route('/stop')      # 웹브라우저가 http://주소/stop을 요청할 때 실행할 함수
def stop():
    global f, html_still, html_record, html, cam
    cam.stop_recording()
    cam.stop_preview()
    cam.close()
    html = '<br><a href="/static/' + f + '">' + f + '</a>' + html
    return html_still + html_record + html

app.run(host='0.0.0.0')
