import socket
import select
import math
from utility import *
import time
 
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
    

   


 
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time)) # run time check
 