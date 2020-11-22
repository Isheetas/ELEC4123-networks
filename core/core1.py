import socket
import select
import math
from utility import *

 
def main():
 
    # 1. Send well-formed HTTP requests
    HOST = '149.171.36.192'
    PORT = 12274
    host = '149.171.36.192' 


    N, e, d = set_key(128) # retrieve 128 bit key values
    '''
    1. Form HTTP Request
    '''
    content = str(N) + "," + str(e)
    request = 'GET / HTTP/1.1\r\nHost: ' + host + '\r\nContent-Length: ' + str(len(content)) + '\r\n\r\n' + content
    request_bytes =  bytes(request, 'utf-8') 


    '''
    2. Request data from Demo Server
    '''
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
    s.close()
    

    '''
    3. Extract Payload
    '''
    # response_tokens = response.split(b'\r\n\r\n') # extract output content - comes after \r\n\r\n
    # response_header = response_tokens[0] + b'\r\n\r\n'
    # payload = response_tokens[1]
    response_split =  split_http_message(response)
    payload = response_split['content']

 
    '''
    4. Resolve Hamming code on payload
    '''
    corrected_databits = hamming_decode(payload)

  
    '''
    5. Decrypt RSA cipher with private key
    '''
    int_cipher = int(corrected_databits, 2)     #convert the bytes into an int, assumed big endian
    decrypted_payload = decrypt_rsa(int_cipher, N, d)

    '''
    6. Display Student Marks
    '''
    print_to_ascii(decrypted_payload)
    
 
def print_to_ascii(msg_bytes):
    n_entries = msg_bytes[0]
    len_student_bytes = 10 # bytes taken up by each students information
    n = 0
    while n < n_entries:
        start = n*10 + 1
        # print(response[i]) 
        # first byte is number of students
        name = str((msg_bytes[start:(start + 5)]), 'utf-8')
        t1 = msg_bytes[start+5]
        t2 = msg_bytes[start+6]
        t3 = msg_bytes[start+7]
        t4 = msg_bytes[start+8]
        total = msg_bytes[start+9]
        print(name, end = ' ')
        print('t1: ',  t1, end = ' ')
        print('t2: ', t2, end = ' ')
        print('t3: ', t3, end = ' ')
        print('t4: ', t4, end = ' ')
        print('total: ', total)
        # next five bytes form name

        n += 1
   


 
if __name__ == '__main__':
    main()
 
 