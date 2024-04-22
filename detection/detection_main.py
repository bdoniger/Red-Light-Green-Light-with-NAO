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
keypoint_history = defaultdict(lambda: [])
gamer_ids = []

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
            if e == "keyboard interrupt":
                conn.close()
                exit()
            continue
    print('[INFO]connected to server...')
    # ping & pong

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
    last_body_angle_list = []
    # camera = Camera_Thread(cv2.VideoCapture(), video=False, video_path=0)
    camera = cv2.VideoCapture(0)
    nao_signal = ""
    is_check = False
    check_time = 0
    signal_trigger = utils.Trigger()
    _,pre_image = camera.read()
    if _ != False:
        model.track(pre_image,device = "cuda",verbose = False)
    try:
        conn.send(("program sign","start"))
    except Exception as e:
        print(e)
        conn.close()
        exit()
    
    while camera.isOpened():
        
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
        # frame = cv2.resize(frame, (360, 640))
        results = model.track(frame,device = "cuda",verbose = False,imgsz=640)   
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
            keypoint = keypoint_history[track_id]
            for i in range(len(skeletons)):
                if utils.check_skeleton_within_bounding_box(skeletons[i],box):
                    body_angle.append(utils.calculate_body_angle(skeletons[i],pose_dict))
                    keypoint.append(skeletons[i])
            if len(body_angle) > 10:
                body_angle.pop(0)
                keypoint.pop(0)
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
        if nao_signal == "check":
            logger.info('check received')
            is_check = True
            check_time = time.time()
            nao_signal = ""
        if is_check :
            logger.info('checking for hand raise')
            gamer_ids = utils.check_hand_raise(keypoint_history,pose_dict)
            print(gamer_ids)
            if gamer_ids == []:
                check_time = time.time()
            if gamer_ids != [] and time.time() - check_time > 2:
                is_check = False
                conn.send(("gamer",len(gamer_ids)))
            
            
            # body_angle_to_check = body_angle_history.items()[:][-1].copy()
            
                
        if nao_signal == "red light":
            logger.info('red light received')
            signal_trigger.rise()
        elif nao_signal == "green light":
            signal_trigger.fall()
        
        if signal_trigger.is_rising_edge():
            
            logger.info("detecting movement...")
            
            try:
                for gamer_id in gamer_ids:
                    last_body_angle = body_angle_history[gamer_id][-1].copy()
                    last_body_angle_list.append(last_body_angle)
            except IndexError:
                last_body_angle = {}
            # print(last_body_angle)
        if signal_trigger.is_triggered():
            for i, gamer_id in enumerate(gamer_ids):
                try :
                    this_body_angle = body_angle_history[gamer_id][-1]
                except IndexError:
                    this_body_angle = {}
                if not utils.check_angle_error_within_threshold(last_body_angle_list[i],this_body_angle,15):
                    logger.info("movement detected")
                    conn.send(("detect",True))
                    
        cv2.imshow("YOLOv8 Pose", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break    
            
            
    
    conn.send(("program sign","stop"))
    # can also send arbitrary objects:

    conn.close()