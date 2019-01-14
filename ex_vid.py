import time
import picamera

cam = picamera.PiCamera()
cam.resolution = (640, 480)
cam.start_preview()
cam.start_recording('f.h264')
time.sleep(5)
cam.stop_recording()
cam.stop_preview()
cam.close()
