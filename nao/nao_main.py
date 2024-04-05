from multiprocessing.connection import Listener
import multiprocessing as mp
import logging
from naoqi import ALProxy
import time

import random
import sys

    
def nao_main():
    address = ('localhost', 6000) 
    listener = Listener(address, authkey=b'secret password')
    conn = listener.accept()
    print 'connection accepted from', listener.last_accepted
    while True:
    
        msg = conn.recv()
        # do something with msg
        print(msg)
        conn.send(("program sign","start"))




ROBOT_ID = "192.168.1.35"
ROBOT_PORT = 9559


def detect_movement(msg):
    if msg == []:
        return False
    if msg[0] == "detect":
        logger.info('received event: %s', msg)
        return msg[1]
    else:
        return False

def detect_touch():
    touchSensors = [
        "Device/SubDeviceList/Head/Touch/Front/Sensor/Value",
        "Device/SubDeviceList/Head/Touch/Rear/Sensor/Value",
        "Device/SubDeviceList/Head/Touch/Middle/Sensor/Value"
    ]

    for sensor in touchSensors:
        if memory.getData(sensor) > 0.0:
            return True
    # pass
    return False

def set_led_color(color):
    if color == "red":
        leds.fadeRGB("AllLeds", 0xFF0000, 0.5)
        tts.say("Red Light")
        conn.send(("event","red light"))
    elif color == "green":
        leds.fadeRGB("AllLeds", 0x00FF00, 0.5) 
        tts.say("Green Light")
        conn.send(("event","green light"))
    else:
        leds.reset("AllLeds")  

def game_logic():
    
    
    
    set_led_color("off")
    start_time = time.time()
    action_time = start_time
    while True:
        current_time = time.time()
        msg = []
        if conn.poll(0):
            msg=conn.recv()
        
        if current_time >= action_time or light is None:
            light = random.choice(["red","green"])
            set_led_color(light)
            action_time = current_time + random.uniform(3,5)           

        if light == "red" and detect_movement(msg):
            tts.say("I detected movement!")
            tts.say("You lost.")
            break
        elif light == "green":
            if detect_touch():
                tts.say("You won!")
                break 
        if time.time() - start_time > 300: # mins
            tts.say("Time's up! You lost.")
            break

if __name__ == "__main__":
    logger = mp.log_to_stderr()
    logger.setLevel(logging.INFO)
    logger.info('logger started')
    
    try:
        leds = ALProxy("ALLeds", ROBOT_ID, ROBOT_PORT)
        tts = ALProxy("ALAnimatedSpeech", ROBOT_ID, ROBOT_PORT)
        memory = ALProxy("ALMemory", ROBOT_ID, ROBOT_PORT)
    except Exception as e:
        print "Could not create proxu to ALModule:,", e
        sys.exit(1)
    
    address = ('localhost', 6000) 
    listener = Listener(address, authkey=b'secret password')
    conn = listener.accept()
    print 'connection accepted from', listener.last_accepted
    conn.send(("program sign","start"))
    
    msg = conn.recv()
    # do something with msg
    print(msg)

    game_logic()
