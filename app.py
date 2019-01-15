# 라즈베리파이 원격 카메라
# 웹브라우저를 통해 라즈베리파이 카메라 사용

# 라이브러리 가져오기
import picamera                     # 라즈베리파이 카메라 모듈
import datetime                     # 현재 날짜와 시간을 알려주는 모듈
import io, time                     # 웹스트리밍을 위한 모듈
from base_camera import BaseCamera  # 웹스트리밍을 위한 모듈
from flask import Flask, Response   # 웹서버 구현을 위한 모듈

# 전역 변수
app = Flask(__name__)               # 웹서버 초기화
f = ''                              # 사진 및 동영상 파일 이름 기억을 위한 변수
cam = picamera.PiCamera()           # 카메라 사용 준비
cam.resolution = (320, 240)         # 카메라 해상도 설정
html_list = ''                                                          # 촬영목록 html 태그 저장을 위한 변수
html_still = '<a href="./still"><button>사진 촬영</button></a> '        # 사진 촬영 버튼 html 태그
html_record = '<a href="./record"><button>녹화 시작</button></a> '      # 녹화 시작 버튼 html 태그
html_stop = '<a href="./stop"><button>녹화 종료</button></a> '          # 녹화 정지 버튼 html 태그
html_stream = '<h1>드론 원격 카메라</h1><img src="/video_feed"><br><br>' # 제목과 스트리밍 html 태그

@app.route('/')                     # 웹브라우저가 http://주소/를 요청할 때 실행할 함수
def home():
    #global html_still, html_record, html_list                           # 전역변수 연결
    return html_stream + html_still + html_record + html_list           # 사진 촬영 버튼과 녹화 시작 버튼 및 촬영 목록을 제공

@app.route('/still')                # 웹브라우저가 http://주소/still을 요청할 때 실행할 함수
def still():
    #global f, html_still, html_record, html_list        # 전역 변수 연결
    global html_list
    f = str(datetime.datetime.now()) + '.jpg'           # 현재 날짜와 시간으로 파일 이름 생성
    cam.start_preview()                                 # 미리보기 시작
    cam.capture('./static/' + f)                        # 사진 촬영(static 디렉토리)
    cam.stop_preview()                                  # 미리보기 종료
    html_list = '<br><a href="/static/' + f + '">' + f + '</a>' + html_list   # 촬영한 사진 파일 링크를 목록에 추가
    return html_stream + html_still + html_record + html_list         # 사진 촬영 버튼과 녹화 시작 버튼 및 촬영 목록을 제공

@app.route('/record')               # 웹브라우저가 http://주소/record를 요청할 때 실행할 함수
def record():
    #global f, html_stop, html_list, cam                 # 전역 변수 연결
    global f
    f = str(datetime.datetime.now()) + '.h264'          # 현재 날짜와 시간으로 파일 이름 생성
    cam.start_preview()                                 # 미리보기 시작
    cam.start_recording('./static/' + f)                # 녹화 시작(static 디렉토리)
    return html_stream + html_stop + html_list                        # 녹화 정지 버튼과 촬영 목록을 제공

@app.route('/stop')                 # 웹브라우저가 http://주소/stop을 요청할 때 실행할 함수
def stop():
    #global f, html_still, html_record, html_list, cam   # 전역 변수 연결
    global html_list
    cam.stop_recording()                                # 녹화 정지
    cam.stop_preview()                                  # 미리보기 종료
    html_list = '<br><a href="/static/' + f + '">' + f + '</a>' + html_list   # 촬영한 동영상 파일 링크를 목록에 추가
    return html_stream + html_still + html_record + html_list         # 사진 촬영 버튼과 녹화 시작 버튼과 촬영 목록을 제공

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
