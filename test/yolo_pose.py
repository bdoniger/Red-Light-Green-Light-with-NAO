from ultralytics import YOLO
import cv2
from collections import defaultdict
import numpy as np
from cap_from_youtube import cap_from_youtube


link = "https://www.youtube.com/watch?v=QZYw0SBqjqI&ab_channel=BodyProject"
# cap = cap_from_youtube(link, "720p")
model = YOLO("yolov8m-pose.pt")
print("-----")
cap = cv2.VideoCapture(2)
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

body_angle_history = defaultdict(lambda: [])
track_history = defaultdict(lambda: [])

def calculate_angle(p1, p2, p3):
    if (p1.any() ==0 or p2.any()==0 or p3.any()==0):
        return -1
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)
    
    # Calculate the angle in radians
    angle_rad = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    
    # Convert to degrees
    angle_deg = np.degrees(angle_rad)
    
    return angle_deg


def calculate_body_angle(skeleton):
    body_angle_dict['l_ear_shoulder_angle']  = calculate_angle(skeleton[pose_dict['LEFT_EAR']],skeleton[pose_dict['LEFT_SHOULDER']],skeleton[pose_dict['RIGHT_SHOULDER']])
    body_angle_dict['r_ear_shoulder_angle'] = calculate_angle(skeleton[pose_dict['RIGHT_EAR']],skeleton[pose_dict['RIGHT_SHOULDER']],skeleton[pose_dict['LEFT_SHOULDER']])
    body_angle_dict['l_shoulder_angle'] = calculate_angle(skeleton[pose_dict['LEFT_ELBOW']],skeleton[pose_dict["LEFT_SHOULDER"]],skeleton[pose_dict['LEFT_HIP']])
    body_angle_dict['r_shoulder_angle'] = calculate_angle(skeleton[pose_dict['RIGHT_ELBOW']],skeleton[pose_dict["RIGHT_SHOULDER"]],skeleton[pose_dict['RIGHT_HIP']])
    body_angle_dict['l_elbow_angle'] = calculate_angle(skeleton[pose_dict['LEFT_SHOULDER']],skeleton[pose_dict['LEFT_ELBOW']],skeleton[pose_dict['LEFT_WRIST']])
    body_angle_dict['r_elbow_angle'] = calculate_angle(skeleton[pose_dict['RIGHT_SHOULDER']],skeleton[pose_dict['RIGHT_ELBOW']],skeleton[pose_dict['RIGHT_WRIST']])
    body_angle_dict['l_hip_angle'] = calculate_angle(skeleton[pose_dict['RIGHT_HIP']],skeleton[pose_dict['LEFT_HIP']],skeleton[pose_dict['LEFT_KNEE']])
    body_angle_dict['r_hip_angle'] = calculate_angle(skeleton[pose_dict['LEFT_HIP']],skeleton[pose_dict['RIGHT_HIP']],skeleton[pose_dict['RIGHT_KNEE']])
    body_angle_dict['l_knee_angle'] = calculate_angle(skeleton[pose_dict['LEFT_HIP']],skeleton[pose_dict['LEFT_KNEE']],skeleton[pose_dict['LEFT_ANKLE']])
    body_angle_dict['r_knee_angle'] = calculate_angle(skeleton[pose_dict['RIGHT_HIP']],skeleton[pose_dict['RIGHT_KNEE']],skeleton[pose_dict['RIGHT_ANKLE']])
    return body_angle_dict

def calculate_body_angle_mean(body_angle_history):
    pass

def check_angle_error_within_threshold(last_body_angle, current_body_angle, threshold):
    for key in last_body_angle.keys():
        if last_body_angle[key] == -1 or current_body_angle[key] == -1:
            continue
        
        print(last_body_angle[key])
        if abs(last_body_angle[key]-current_body_angle[key]) > threshold:
            print(f"Error in {key} angle")
            print(f"Last angle: {last_body_angle[key]}")
            print(f"Current angle: {current_body_angle[key]}")
            return False
    return True

def check_within_bounding_box(x,y,box):
    if x ==0 or y == 0:
        return True
    x_center, y_center, w, h = box
    x_min = x_center - w/2
    x_max = x_center + w/2
    y_min = y_center - h/2
    y_max = y_center + h/2
    if x_min <= x <= x_max and y_min <= y <= y_max:
        return True
    return False

def check_skeleton_within_bounding_box(skeleton,box):
    for i in range(17):
        if not check_within_bounding_box(skeleton[i][0],skeleton[i][1],box):
            return False
    return True




last_body_angle = body_angle_dict
c_press = False
def press(key,last_body_angle,angle):
    print(f"'{key}' pressed")
    if key == "c":
       last_body_angle = angle 
while cap.isOpened():
    success, frame = cap.read()
    if success:
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
                if check_skeleton_within_bounding_box(skeletons[i],box):
                    body_angle.append(calculate_body_angle(skeletons[i]))
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
    #check if c is pressed
        if cv2.waitKey(1) & 0xFF == ord("c"):
            print("c pressed")
            #average of last 5 frames
            
            # last_body_angle = np.mean(body_angle_history[1][-5:],axis=0)
            last_body_angle = body_angle_history[1][-1].copy()
            print(last_body_angle)
            c_press = True
        if c_press and (not check_angle_error_within_threshold(last_body_angle,body_angle_history[1][-1],10)):
            print("move!!")
            break
       

        cv2.imshow("YOLOv8 Pose", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break