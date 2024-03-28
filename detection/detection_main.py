from multiprocessing.connection import Client
import multiprocessing as mp
from multiprocessing.connection import Connection, _ForkingPickler, Client, Listener
import os

# override library's reducer
def send_py2(self, obj):
    self._check_closed()
    self._check_writable()
    self._send_bytes(_ForkingPickler.dumps(obj, protocol=2))

Connection.send = send_py2
# override library's reducer



if __name__ == '__main__':
    
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
    
    
    
    conn.send('close')
    # can also send arbitrary objects:
    conn.send(['a', 2.5, None, int, sum])
    conn.close()