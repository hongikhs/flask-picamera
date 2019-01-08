import os
import time
import picamera
import datetime
import paho.mqtt.client as mqtt

st = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("cam")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global st
    
    print(msg.topic+" "+str(msg.payload))

    cmd = int(msg.payload)
    print(cmd)
    
    if cmd == 2:
        f = str(datetime.datetime.now()) + '.jpg'
        camera.capture(f)
        st = time.time()
        os.system('rclone copy . remotecam:')
        print(time.time() - st)
        print(f + ' saved.')
    elif cmd == 1:
        f = str(datetime.datetime.now()) + '.h264'
        camera.start_recording(f)
        print('start recording : ' + f)
    elif cmd == 0:
        camera.stop_recording()
        os.system('rclone copy . remotecam:')
        print(f + ' saved.')

camera = picamera.PiCamera()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set('stu00', password='dent00')
client.connect("hicode.space", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
