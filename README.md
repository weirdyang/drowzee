
# drowzee
Flask app using opencv for drowsiness detection

This is built using [miguelgrinberg\'s flask video streaming example](https://github.com/miguelgrinberg/flask-video-streaming/tree/v1).

Articles:

* [video streaming with Flask](http://blog.miguelgrinberg.com/post/video-streaming-with-flask) 
* follow-up [Flask Video Streaming Revisited](http://blog.miguelgrinberg.com/post/flask-video-streaming-revisited).

## Description

The app will try to detect faces and eyes. If it detects 50 frames of faces with no eyes consecutively, it will play a sound and deduct a score.

## Libraries used

Pygame, Flask, PyFladesk, OpenCV and pyinstaller

pyinstaller build command:

    pyinstaller -w --add-data "templates;templates" --add-data "static;static" app.py --path 'C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64'   
    
or if you downloaded the app.spec:

    pyinstaller app.spec
      
## References: 

[Face Detection using Haar Cascades - OpenCV tutorial](https://docs.opencv.org/3.3.0/d7/d8b/tutorial_py_face_detection.html)
