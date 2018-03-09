# drowzee
Flask app using opencv for drowsiness detection

This is built using [https://github.com/miguelgrinberg/flask-video-streaming/tree/v1](miguelgrinberg's flask video streaming example).

## Description

The app will try to detect faces and eyes. If it detects 5 frames of faces with no eyes consecutively, it will play a sound and deduct a score.

## Libraries used

Pygame, Flask, OpenCV and pyinstaller

pyinstaller build command:

    pyinstaller -w --add-data "templates;templates" --add-data "static;static" app.py --hidden-import  ctypes --path 'C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64'   
      
References: 

[Face Detection using Haar Cascades - OpenCV tutorial](https://docs.opencv.org/3.3.0/d7/d8b/tutorial_py_face_detection.html)


