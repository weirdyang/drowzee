#!/usr/bin/env python
from importlib import import_module
import os
import sys
from flask import Flask, render_template, Response
from pyfladesk import init_gui
from camera import Camera, resource_path
##C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64 <<-add to path when building

'''tell flask where too look for resources
if this is bundled in 1 file'''
if getattr(sys, 'frozen', False):
    template_folder =resource_path('templates')
    static_folder = resource_path('static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
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
@app.route('/restart', methods=['POST'])
def restart():
    """restarts camera"""
    webcam = Camera()
    return "Camera restarted"

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(response=gen(webcam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    init_gui(app, port=5000, width=640, height=800,
             window_title="PyFladesk",icon="appicon.png", argv=None)
