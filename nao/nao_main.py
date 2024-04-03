from multiprocessing.connection import Listener

    


if __name__ == '__main__':
    pass
    # establish connection with the server
    address = ('localhost', 6000) 
    listener = Listener(address, authkey=b'secret password')
    conn = listener.accept()
    print 'connection accepted from', listener.last_accepted
    while True:
    
        msg = conn.recv()
        # do something with msg
        print(msg)
        conn.send(("program sign","start"))