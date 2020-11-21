# create server and client
import socket
import select
from ext2_utility import *


def get_student_payload(HOST_server, PORT_d, n_students):
        #Request message from data server
    content = '4,' + str(n_students) 
    request_bytes =  bytes(content, 'utf-8')

    try:
        s_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("Socket successfully created to data server")
    except socket.error as err:
        print ("socket creation failed with error %s to data server" %(err))

    s_data.connect((HOST_server, PORT_d))
    s_data.send (request_bytes)

    #s.send (request_bytes)
    ready = select.select([s_data], [], [], 10)
    if ready[0]:
        response = s_data.recv(64000)

    s_data.close()

    print(response)
    return response



def main():
    #CREATE SERVER
    HOST = '127.0.0.1'
    PORT = 3000
    HOST_data_server = '149.171.36.192'
    PORT_data_server = 12000


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((HOST, PORT))
    s.listen(5)
    while True:

        conn, addr = s.accept()
        print(f"Connection from {addr} has been established.")
        
        '''
        1. get public keys from client
        '''  
        key = conn.recv(1024)
        key = str(key)
        key = key[2:len(key)-1]
        key_split = key.split(',')
        n = int(key_split[0])
        #print(n)
        e = int(key_split[1])
        #print(e)

        
        '''
        2. get an unencrypted payload from the data server
        '''
        payload =  get_student_payload(HOST_data_server, PORT_data_server, 100) # last arg is int value of num of students


        '''
        3. encrypt payload with public keys and send to client
        '''
        cipher = encrypt_rsa(payload, n, e)
        conn.sendall(cipher)


if __name__ == '__main__':
    main()
 