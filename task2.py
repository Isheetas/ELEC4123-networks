import socket
import select
import json
import struct
from utility import *
import time


'''
task 2 server
functions needed: 
    - add hamming code (parity bits) (input: binary, output: binary)
    - decode hamming code (to get the message) (input: binary, output: binary)
    - encrypt RSA
    - decrypt RSA
    - change data

Questions: 
    - is our socket meant to be listening to arash's socket 
     (to see when arahs' client has requested marks) -> in that case, would our program be a server?
      because -> Arash's client returns a GET request with N and e

'''

def main():
    # these values will be recieved from client
    N = 252837207378338387332619197259204540353
    e = 65537
    d = 48393883292703003300067554859838128129

    HOST = '149.171.36.192'
    PORT_client = 12275
    PORT_db = 12274

    '''
    -1. Get data from arash's client
    '''

    try: 
        s_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print ("Socket successfully created to Arash")
    except socket.error as err: 
        print ("socket creation failed with error %s to Arash" %(err))
    s_client.connect((HOST, PORT_client))
    #s_client.send (req_bytes)

    ready = select.select([s_client], [], [], 10)
    if ready[0]:
        response = s_client.recv(64000)
        print('response from arash client: ', response) 

    s_client.close

    response_tokens = response.split(b'\r\n\r\n')
    response_header = response_tokens[0] + b'\r\n\r\n'
    #print(b'response header:' + response_header)
    payload = str(response_tokens[1])
    payload = payload[2:len(payload)-1]
    

    payload_split = payload.split(',')
    N_client = int(payload_split[0])
    e_client = int(payload_split[1])




    '''
    0. send request to client (db?) and get message
    '''

    
    # return message header for future use as we
    response = get_data_from_db(HOST, PORT_db, N, e, d)
    msg = response.get_content()
    msg_bin = bytes_to_bits(msg)
    # msg_bin = convert_payload_binary(msg)
    corrected_msg = hamming(msg_bin)
    corrected_msg = int(corrected_msg, 2)

    # decrypt_msg = decrypt_rsa(msg_bytes, N, d)
    decrypt_msg = decrypt_rsa(corrected_msg, N, d)

    print('dec msg: ', decrypt_msg)

    '''
    1. Create a database class
    '''
    db = create_db(decrypt_msg)
    #print('before: ', db.json())

    '''
    2. Alter database
    '''
    db.change_marks()
    #print('after: ', db.json())

    '''
    3. Convert db to bytes
    '''
    changed_bytes = db.get_bytes()

    '''
    4. Hamming encode
    '''
    hamming_bin = hamming_encode(changed_bytes)
    hamming_int = int(hamming_bin)

    '''
    5. Encrypt with rsa
    '''
    modified_msg = encrypt_rsa(hamming_int, N, e)
    print('to send: ', modified_msg)

    '''
    6. construct response and sent to user
    '''
    response.set_content(modified_msg)
    print('full response string:', response.as_string())
    


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time)) # run time check