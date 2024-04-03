from multiprocessing.connection import Client
import multiprocessing as mp
import logging
from multiprocessing.connection import Connection, _ForkingPickler, Client, Listener
import time
import os
from camera import Camera_Thread
from ultralytics import YOLO
import cv2
from collections import defaultdict
import numpy as np
from cap_from_youtube import cap_from_youtube
import utils

## hack to make it work with python 2.7
# override library's reducer
def send_py2(self, obj):
    self._check_closed()
    self._check_writable()
    self._send_bytes(_ForkingPickler.dumps(obj, protocol=2))

Connection.send = send_py2
# override library's reducer



pose_dict = {
    'NOSE':           0,
    'LEFT_EYE':       1,
    'RIGHT_EYE':      2,
    'LEFT_EAR':       3,
    'RIGHT_EAR':      4,
    'LEFT_SHOULDER':  5,
    'RIGHT_SHOULDER': 6,
    'LEFT_ELBOW':     7,
    'RIGHT_ELBOW':    8,
    'LEFT_WRIST':     9,
    'RIGHT_WRIST':    10,
    'LEFT_HIP':       11,
    'RIGHT_HIP':      12,
    'LEFT_KNEE':      13,
    'RIGHT_KNEE':     14,
    'LEFT_ANKLE':     15,
    'RIGHT_ANKLE':    16}

body_angle_dict={'l_ear_shoulder_angle':-1,
                 'r_ear_shoulder_angle':-1,
                    'l_shoulder_angle':-1,
                    'r_shoulder_angle':-1,
                    'l_elbow_angle':-1,
                    'r_elbow_angle':-1,
                    'l_hip_angle':-1,
                    'r_hip_angle':-1,
                    'l_knee_angle':-1,
                    'r_knee_angle':-1
                 }
model = YOLO("yolov8m-pose.pt") 
body_angle_history = defaultdict(lambda: [])
track_history = defaultdict(lambda: [])

if __name__ == '__main__':
    

    
    # logger
    logger = mp.log_to_stderr()
    logger.setLevel(logging.INFO)
    logger.info('logger started')
    
    # establish connection with the server
    address = ('localhost', 6000)
    conn = []
    while conn == []:
        try:
            print('[INFO]try to connect to server...')
            conn = Client(address, authkey=b'secret password')
        except Exception as e:
            print(e)
            os.system('sleep 1')
            continue
    print('[INFO]connected to server...')
    # ping & pong
    try:
        conn.send(("program sign","start"))
    except Exception as e:
        print(e)
        conn.close()
        exit()
    try:
        conn_sign = conn.recv()
    except Exception as e:
        print(e)
        conn.close()
        exit()
    # camera
    if conn_sign[0] == "program sign":
        if conn_sign[1] == "start":
            logger.info('send & recv good')
    
    
    last_body_angle = body_angle_dict
    camera = Camera_Thread(cv2.VideoCapture(0), video=False, video_path=0)
    nao_signal = ""
    signal_trigger = utils.Trigger()
    while camera.is_open():
        
        if conn.poll(0):
            msg = conn.recv()
            if msg[0] == "event":
                nao_signal = msg[1]
                logger.info('received event: %s', nao_signal)
            elif msg[0] == "program sign":
                if msg[1] == "stop":
                    logger.info('received stop signal')
                    break
            else:
                pass
            
          
        success, frame = camera.read()
        if not success:
            camera.release()
            logger.error('camera broken')
            break
        
        results = model.track(frame,device = "cuda",verbose = False)   
        annotated_frame = results[0].plot()
        boxes = results[0].boxes.xywh.cpu()
        try:
            track_ids = results[0].boxes.id.int().cpu().tolist()
        except AttributeError:
            track_ids = []
        try:
            skeletons = results[0].keypoints.xy.cpu().numpy()
        except AttributeError:
            skeletons = []
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            track = track_history[track_id]
            track.append((float(x), float(y)))
            body_angle=body_angle_history[track_id]
            for i in range(len(skeletons)):
                if utils.check_skeleton_within_bounding_box(skeletons[i],box):
                    body_angle.append(utils.calculate_body_angle(skeletons[i],pose_dict))
            if len(body_angle) > 10:
                body_angle.pop(0)
            if len(track) > 90:
                track.pop(0)
                

            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(
                annotated_frame,
                [points],
                isClosed=False,
                color=(230, 230, 230),
                thickness=10,
            )
            
            if nao_signal == "stop":
                signal_trigger.rise()
            else:
                signal_trigger.fall()
            
            if signal_trigger.is_rising_edge():
                last_body_angle = body_angle_history[1][-1].copy()
                print(last_body_angle)
            if signal_trigger.is_triggered():
                if not utils.check_angle_error_within_threshold(last_body_angle,body_angle_history[1][-1],10):
                    logger.info("movement detected")
                    conn.send(("detect",True))
            
            
            
    
    conn.send(("program sign","stop"))
    # can also send arbitrary objects:

    conn.close()