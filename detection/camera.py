import cv2
import numpy as np
import yaml
import time
from datetime import datetime



class Camera_Thread(object):
    def __init__(self, capture_method, video=False, video_path=None):
        '''
        the Camera_Thread class which will restart camera when it broken

        :param capture_method: the method to open the camera(a function)
        :param video: use video or not
        :param video_path: video path

        '''
        self._date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        self._open = False
        self._cap = None
        self._is_init = False
        self._video = video
        self._video_path = video_path
        self._capture_method = capture_method
        # try to open it once
        self.open()

    def open(self):
        # if camera not open, try to open it
        if not self._video:
            if not self._open:
                self._open= self._capture_method(self._video_path).isopened()
                self._cap = self._capture_method(self._video_path)
                if not self._is_init and self._open:
                    self._is_init = True
        else:
            if not self._open:
                self.cap = cv2.VideoCapture(self._video_path)
                self._open = True
                print("[INFO] open video {0}".format(self._video_path))
                if not self._is_init and self._open:
                    self._is_init = True

    def is_open(self):
        '''
        check the camera opening state
        '''
        return self._open

    def read(self):
        if self._open:
            r, frame = self.cap.read()
            if not r:
                self.cap.release()  # release the failed camera
                self._open = False
            return r, frame
        else:
            return False, None

    def release(self):
        if self._open:
            self.cap.release()
            self._open = False

    def __del__(self):
        if self._open:
            self.cap.release()
            self._open = False