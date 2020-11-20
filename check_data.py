'''
Dummy file to get samples 
'''

import socket
import select
def main():
 
    # 1. Send well-formed HTTP requests
    HOST = '149.171.36.192'
    PORT = 12000
    content = '4,100'
 
    # HTTP request headers
    #request = 'GET / HTTP/1.1\r\nHost: ' + HOST + '\r\nContent-Length: ' + str(len(content)) + '\r\n\r\n' + content
    request_bytes =  bytes(content, 'utf-8') 
    print(content)

    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print ("Socket successfully created")
    except socket.error as err: 
        print ("socket creation failed with error %s" %(err))

    s.connect((HOST, PORT))
    s.send (request_bytes)
    
    ready = select.select([s], [], [], 10)
    if ready[0]:
        response = s.recv(64000)

    print(response)

    #print(repr(response))
    print(response)


if __name__ == '__main__':
    main()
 