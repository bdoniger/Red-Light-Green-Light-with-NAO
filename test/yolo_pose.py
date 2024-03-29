from ultralytics import YOLO
import cv2
from collections import defaultdict
import numpy as np
from cap_from_youtube import cap_from_youtube

link = "https://www.youtube.com/watch?v=QZYw0SBqjqI&ab_channel=BodyProject"
cap = cap_from_youtube(link, "720p")
model = YOLO("yolov8m-pose.pt")

# cap = cv2.VideoCapture(0)
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
                 }

body_angle_history = defaultdict(lambda: [])


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
    l_ear_shoulder_angle = calculate_angle(skeleton[0][pose_dict['LEFT_EAR']],skeleton[0][pose_dict['LEFT_SHOULDER']],skeleton[0][pose_dict['RIGHT_SHOULDER']])
    r_ear_shoulder_angle = calculate_angle(skeleton[0][pose_dict['RIGHT_EAR']],skeleton[0][pose_dict['RIGHT_SHOULDER']],skeleton[0][pose_dict['LEFT_SHOULDER']])
    l_shoulder_angle = calculate_angle(skeleton[0][pose_dict['LEFT_ELBOW']],skeleton[0][pose_dict["LEFT_SHOULDER"]],skeleton[0][pose_dict['LEFT_HIP']])
    r_shoulder_angle = calculate_angle(skeleton[0][pose_dict['RIGHT_ELBOW']],skeleton[0][pose_dict["RIGHT_SHOULDER"]],skeleton[0][pose_dict['RIGHT_HIP']])
    l_elbow_angle = calculate_angle(skeleton[0][pose_dict['LEFT_SHOULDER']],skeleton[0][pose_dict['LEFT_ELBOW']],skeleton[0][pose_dict['LEFT_WRIST']])
    r_elbow_angle = calculate_angle(skeleton[0][pose_dict['RIGHT_SHOULDER']],skeleton[0][pose_dict['RIGHT_ELBOW']],skeleton[0][pose_dict['RIGHT_WRIST']])
    l_hip_angle = calculate_angle(skeleton[0][pose_dict['RIGHT_HIP']],skeleton[0][pose_dict['LEFT_HIP']],skeleton[0][pose_dict['LEFT_KNEE']])
    r_hip_angle = calculate_angle(skeleton[0][pose_dict['LEFT_HIP']],skeleton[0][pose_dict['RIGHT_HIP']],skeleton[0][pose_dict['RIGHT_KNEE']])
    l_knee_angle = calculate_angle(skeleton[0][pose_dict['LEFT_HIP']],skeleton[0][pose_dict['LEFT_KNEE']],skeleton[0][pose_dict['LEFT_ANKLE']])
    r_knee_angle = calculate_angle(skeleton[0][pose_dict['RIGHT_HIP']],skeleton[0][pose_dict['RIGHT_KNEE']],skeleton[0][pose_dict['RIGHT_ANKLE']])
    pass

   
while cap.isOpened():
    success, frame = cap.read()
    if success:
        results = model.predict(frame,device = "cuda",verbose = False)
        annotated_frame = results[0].plot()
        boxes = results[0].boxes.xywh.cpu()
        #check type of boxes
        # print(type(boxes))
        # track_ids = results[0].boxes.id.int().cpu().tolist()
        skeleton = results[0].keypoints.xy.cpu().numpy()
        print(skeleton.shape)
        l_ear_shoulder_angle = calculate_angle(skeleton[0][pose_dict['LEFT_EAR']],skeleton[0][pose_dict['LEFT_SHOULDER']],skeleton[0][pose_dict['RIGHT_SHOULDER']])

        cv2.imshow("YOLOv8 Pose", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break