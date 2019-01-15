import io, time                     # 웹스트리밍을 위한 모듈
from base_camera import BaseCamera  # 웹스트리밍을 위한 모듈
from flask import Flask, Response   # 웹서버 구현을 위한 모듈

# 전역 변수
app = Flask(__name__)               # 웹서버 초기화
cam = picamera.PiCamera()           # 카메라 사용 준비
cam.resolution = (320, 240)         # 카메라 해상도 설정

html_stream = '<h1>드론 원격 카메라</h1><img src="/video_feed"><br><br>' # 제목과 스트리밍 html 태그

@app.route('/')                     # 웹브라우저가 http://주소/를 요청할 때 실행할 함수
def home():
    return html_stream

@app.route('/still')                # 웹브라우저가 http://주소/still을 요청할 때 실행할 함수
def still():
    return html_stream

@app.route('/record')               # 웹브라우저가 http://주소/record를 요청할 때 실행할 함수
def record():
    return html_stream

@app.route('/stop')                 # 웹브라우저가 http://주소/stop을 요청할 때 실행할 함수
def stop():
    return html_stream

# 웹스트리밍을 위한 코드
class Camera(BaseCamera):
    @staticmethod
    def frames():
        time.sleep(2)
        stream = io.BytesIO()
        for _ in cam.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            yield stream.read()
            stream.seek(0)
            stream.truncate()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')           # 웹브라우저가 http://주소/video_feed를 요청할 때 실행할 함수 
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
