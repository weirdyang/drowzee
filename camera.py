import threading
import os
import sys
import time

import cv2

import _thread
from audiopy import start_player
from base_camera import BaseCamera

basedir = os.path.abspath(os.path.dirname(__file__))
##https://irwinkwan.com/2013/04/29/python-executables-pyinstaller-and-a-48-hour-game-design-compo/
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

def checking_video_source():
    for x in range(2, -1, -1):
        camera = cv2.VideoCapture(x)
        if camera.isOpened():
            print('Video source is {}'.format(x))
            break
    return camera



class Camera(BaseCamera):
    video_source = 0
    score = 100
    classifier = 0
    time_start = None
    time_end = None

    @staticmethod
    def set_time_start(timestamp):
        Camera.time_start = timestamp
    
    @staticmethod
    def set_time_end(timestamp):
        Camera.time_end = timestamp
    
    @staticmethod
    def get_duration():
        duration = Camera.time_end - Camera.time_start
        total_hour = (duration.total_seconds())/ 60 / 60
        return round(total_hour, 3)

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def set_classifier(status):
        Camera.classifier = status

    @staticmethod
    def camera_reset():
        Camera.score = 100

    @staticmethod
    def get_score():
        return Camera.score

    @staticmethod
    def frames():
        '''Captures stream frame by frame and passes it
        to the classifier
        '''
        wakeup = resource_path(os.path.join('static', 'wakeup.mp3'))
        takeabreak = resource_path(os.path.join('static', 'takeabreak.mp3'))
        gameover = resource_path(os.path.join('static', 'gameover.mp3'))
        face_cascade = cv2.CascadeClassifier(resource_path(os.path.join('static', 'haarcascade_frontalface_alt.xml')))
        eye_cascade = cv2.CascadeClassifier(resource_path(os.path.join('static','parojosG.xml')))
        camera = checking_video_source()
        print(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        counter = 0
        alarm = 0
        while True:
            # Capture frame-by-frame
            
            ret, frame = camera.read()
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            height, width, channels = frame.shape 
            #https://docs.opencv.org/master/d6/d00/tutori al_py_root.html
            faces = face_cascade.detectMultiScale(gray,
                                      scaleFactor=1.1,
                                      minNeighbors=3,
                                      minSize=(100, 100),
                                      flags=cv2.CASCADE_SCALE_IMAGE)
    
            font = cv2.FONT_HERSHEY_SIMPLEX
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=4,
                                                    flags=cv2.CASCADE_FIND_BIGGEST_OBJECT)
                if Camera.classifier == 1:
                    if(not len(eyes)):
                        cv2.putText(frame, 'Sleeping', (25, 25), font,
                                1, (255, 255, 255), 2, cv2.LINE_AA)
                        counter += 1
                        if counter == 50:
                            Camera.score -= 20
                            alarm += 1
                            if alarm == 5:
                                try:
                                    playthread = threading.Thread(target=start_player, args=(gameover,) )
                                    playthread.start()
                                except Exception as e:
                                    print(e)
                            elif alarm >= 3:
                                try:
                                    playthread = threading.Thread(target=start_player, args=(takeabreak,) )
                                    playthread.start()
                                except Exception as e:
                                    print(e)
                            else:
                                try:
                                    playthread = threading.Thread(target=start_player, args=(wakeup,) )
                                    playthread.start()
                                except Exception as e:
                                    print(e)
                            counter = 0
                            
                    else:
                        cv2.putText(frame, 'Awake', (25, 25), font,
                            1, (255, 255, 255), 2, cv2.LINE_AA)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            cv2.putText(frame, '{}'.format(Camera.score), (25, height-25), font, 1, (255,0,255), 2, cv2.LINE_AA)
            if Camera.score < 80:
                cv2.rectangle(frame, (0,height), (0+2*Camera.score, height-25), (0,255,255), -1)   
            else:
                cv2.rectangle(frame, (0,height), (0+2*Camera.score, height-25), (124,252,0), -1)
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', frame)[1].tobytes()
