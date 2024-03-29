from multiprocessing.connection import Listener

address = ('localhost', 6000)     
listener = Listener(address, authkey=b'secret password')
conn = listener.accept()
print 'connection accepted from', listener.last_accepted
while True:
    
    msg = conn.recv()
    # do something with msg
    print(msg)
listener.close()