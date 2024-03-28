from multiprocessing.connection import Listener

    


if __name__ == '__main__':
    pass
    # establish connection with the server
    address = ('localhost', 6000) 
    listener = Listener(address, authkey=b'secret password')
    conn = listener.accept()