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


    # pass
    return False

def set_led_color(color):
    if color == "red":
        conn.send(("event","red light"))
    elif color == "green":
        conn.send(("event","green light"))
    else:
        pass

def check_participant():
    print("Checking for participant")
    
    msg = []
    conn.send(("event","check"))
    print("Sent check event")
    msg = conn.recv()
    if msg[0] == "gamer":
        return True
    

def game_logic():
    # tts.say("Hello, welcome to the red light green light game!")
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
            action_time = current_time + random.uniform(2,3)           

        if light == "red" and detect_movement(msg):
            break
        elif light == "green" and detect_touch():
                break 
        if time.time() - start_time > 60: # mins

            break

if __name__ == "__main__":
    logger = mp.log_to_stderr()
    logger.setLevel(logging.INFO)
    logger.info('logger started')
    

    
    address = ('localhost', 6000) 
    listener = Listener(address, authkey=b'secret password')
    conn = listener.accept()
    print 'connection accepted from', listener.last_accepted
    conn.send(("program sign","start"))
    
    msg = conn.recv()
    # do something with msg
    print(msg)
    check_participant()
    game_logic()
