import numpy as np
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


def calculate_body_angle(skeleton,pose_dict):
    body_angle_dict = {}
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


def check_hand_raise(skeletons,pose_dict):
    if skeletons == {}:
        return []
    keys = list(skeletons.keys())
    values = list(skeletons.values())[-1]

    ids=[]
    for id,skeleton in zip(keys,values):
        
        # print(skeleton[pose_dict['RIGHT_WRIST']][1],skeleton[pose_dict['RIGHT_SHOULDER']][1])
        if (skeleton[pose_dict['LEFT_WRIST']].any()==0 or skeleton[pose_dict['LEFT_SHOULDER']].any()==0) or (skeleton[pose_dict['RIGHT_WRIST']].any()==0 or skeleton[pose_dict['RIGHT_SHOULDER']].any()==0):
            continue
        if (skeleton[pose_dict['LEFT_WRIST']][1] < skeleton[pose_dict['LEFT_SHOULDER']][1]) or (skeleton[pose_dict['RIGHT_WRIST']][1] < skeleton[pose_dict['RIGHT_SHOULDER']][1]):
            ids.append(id)
            print(f"Hand raised by {id}")
    return ids


def check_angle_error_within_threshold(last_body_angle, current_body_angle, threshold):
    if last_body_angle == {} or current_body_angle == {}:
        return True
    for key in last_body_angle.keys():
        if last_body_angle[key] == -1 or current_body_angle[key] == -1:
            continue
        
        # print(last_body_angle[key])
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

class Latch():
    def __init__(self):
        self.lock = False
    def lock(self):
        self.lock = True
    def release(self):
        self.lock = False
    def is_locked(self):
        return self.lock
    
class Trigger():
    def __init__(self):
        self.trigger = False
        self.last_trigger = False
    def rise(self):
        self.trigger = True
    def fall(self):
        self.trigger = False
    def is_rising_edge(self):
        if self.trigger and not self.last_trigger:
            self.last_trigger = self.trigger
            return True
        else:
             self.last_trigger = self.trigger
        return False
    def is_triggered(self):
        return self.trigger
        
