#client for extension task 1
import socket
import time
from ext2_utility import *



def main():

    '''
    local server details
    '''    
    HOST = '127.0.0.1'
    PORT = 3000


    '''
    public and private keys
    '''
    #client sends 'n,e'
    n = '252837207378338387332619197259204540353'
    d = '48393883292703003300067554859838128129'
    e = '65537'



    '''
    1. Request data from client
    '''
    request = n + ',' + e
    request_bytes = bytes(request, 'utf-8')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))

    s.connect((HOST, PORT))
    s.send(request_bytes)
    data = s.recv(1024)
    s.close()
    print('Received', repr(data))

    '''
    Decrypt recieved data
    '''
    plaintext = decrypt_rsa(data, n, d)

    #display data
    print_to_ascii(plaintext)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time)) # run time check
 