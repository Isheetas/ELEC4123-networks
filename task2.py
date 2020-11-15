import socket
import select
import json
import struct
from utility import *

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

    

    msg = get_data_from_db(HOST, PORT_db, N, e, d)
    msg_bin = convert_payload_binary(msg)
    corrected_msg = hamming(msg_bin)
    corrected_msg = int(corrected_msg, 2)
    msg_bytes = corrected_msg.to_bytes((corrected_msg.bit_length() + 7) // 8, 'big')

    decrypt_msg = decrypt_rsa(msg_bytes, N, d)

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
    changed_bytes = db.to_bytes()

    '''
    4. Hamming encode
    '''
    hamming_bin = hamming_encode(changed_bytes)
    hamming_int = int(hamming_bin)

    '''
    5. Encrypt with rsa
    '''
    send_byte = encrypt_rsa(hamming_int, N, e)
    print('to send: ', send_byte)

    '''
    6. construct response and sent to user
    '''
    
    



def bytes_to_int(byte):
    print('in bytes->int')
    fin = ""
    print(len(byte))
    for i in byte:
        binary = bin(i)
        binary = binary[2:]
        fin = fin + binary.zfill(8) 
    print(fin, len(fin))

    integer = int(fin, 2)
    print('integer: ', integer)


    return integer

def int_to_bytes(integer):
    '''
    input: int
    output: list of bytes(binary) - WHAT IF NOT DIVISIBLE BY 8????
    '''

    binary = bin(integer)       #return binary of integers in string format 
    binary = binary[2:]         #chop off the first two element (0b)

    print('bin: ', integer)
    list_of_bytes = []          #will contain whole binary into list of 8bits (string)
    n = 8
    list_of_bytes = [binary[i:i+8] for i in range(0, len(binary), n)]

    print('list of bytes: ', list_of_bytes)
        
    return list_of_bytes
    

if __name__ == '__main__':
    main()