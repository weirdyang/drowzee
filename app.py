#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
from pyfladesk import init_gui

##C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64 <<-add to path when building

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)
webcam = Camera()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/start', methods=["POST"])
def start():
    """start scoring - turn on eye classifier"""
    webcam.set_classifier(1)
    return "Classifier ON - Status {}".format(webcam.classifier)

@app.route('/stop', methods=["POST"])
def stop():
    """start scoring - turn on eye classifier"""
    webcam.set_classifier(0)
    final = webcam.get_score()
    webcam.camera_reset()
    return "Final Score: {}".format(final)



def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(webcam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    init_gui(app, port=5000, width=640, height=700,
             window_title="PyFladesk",icon="appicon.png", argv=None)
