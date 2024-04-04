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
    if msg[0] == "detect":
        logger.info('received event: %s', msg)
        return msg[1]
    else:
        return False

def detect_touch():
    # pass
    return False

def set_led_color(color):
    if color == "red":
        leds.fadeRGB("AllLeds", 0xFF0000, 0.5)
        tts.say("Red Light")
    elif color == "green":
        leds.fadeRGB("AllLeds", 0x00FF00, 0.5) 
        tts.say("Green Light")
    else:
        leds.reset("AllLeds")  

def game_logic():
    address = ('localhost', 6000) 
    listener = Listener(address, authkey=b'secret password')
    conn = listener.accept()
    print 'connection accepted from', listener.last_accepted
    msg = conn.recv()
    # do something with msg
    print(msg)
    conn.send(("program sign","start"))
    
    
    set_led_color("off")
    start_time = time.time()
    while True:
        if conn.poll(0):
            msg=conn.recv()
                   
        # light = random.choice(["red","green"])
        light = "red"
        if light == "red":
            conn.send(("event","red light"))
        else:
            conn.send(("event","green light"))
        
        set_led_color(light)
        time.sleep(max(1.5,random.uniform(1.5,3)))

        if light == "red" and detect_movement(msg):
            tts.say("I detected movement!")
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
        tts = ALProxy("ALTextToSpeech", ROBOT_ID, ROBOT_PORT)
    except Exception as e:
        print "Could not create proxu to ALModule:,", e
        sys.exit(1)

    game_logic()
