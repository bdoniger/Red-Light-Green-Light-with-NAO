from multiprocessing.connection import Client
import multiprocessing as mp
import logging
from multiprocessing.connection import Connection, _ForkingPickler, Client, Listener
import time
import os
from camera import Camera_Thread

## hack to make it work with python 2.7
# override library's reducer
def send_py2(self, obj):
    self._check_closed()
    self._check_writable()
    self._send_bytes(_ForkingPickler.dumps(obj, protocol=2))

Connection.send = send_py2
# override library's reducer





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
    
    
    
    
    
    conn.send('close')
    # can also send arbitrary objects:
    conn.send(['a', 2.5, None, int, sum])
    conn.close()