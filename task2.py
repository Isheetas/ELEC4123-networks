import socket
import select
import json
import struct
from utility import *
from type_conversions import *
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
    
    HOST = '149.171.36.192'
    PORT_client = 12275
    PORT_db = 12274

    

    
    #1. Get data from arash's client
    
    try: 
        s_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print ("Socket successfully created to Arash")
    except socket.error as err: 
        print ("socket creation failed with error %s to Arash" %(err))
    s_client.connect((HOST, PORT_client))

    ready = select.select([s_client], [], [], 10)
    if ready[0]:
        response = s_client.recv(64000)
        print('response from arash client: ', response) 

    s_client.close

    response_tokens = response.split(b'\r\n\r\n')
    response_header = response_tokens[0] + b'\r\n\r\n'
    payload = str(response_tokens[1])
    payload = payload[2:len(payload)-1]
    

    payload_split = payload.split(',')
    N_client = int(payload_split[0])
    e_client = int(payload_split[1])

    #print("n:", N_client)
    #print("e:", e_client)

    key_size = len(str(bin(N_client))) -2

    N, e, d = set_key(key_size)             #depending on key size - choose our N and e to send to database



    #2. send request to database with YOUR set key and get message
    
    response = get_data_from_db(HOST, PORT_db, N, e, d)
    msg = response.get_content()
    header = response.get_header()                              # return message header for future use as we

    corrected_msg = hamming_decode(msg)
    corrected_msg = int(corrected_msg, 2)

    decrypt_msg = decrypt_rsa(corrected_msg, N, d)


    #1. Create database class
    db = create_db(decrypt_msg)
    #print('before: ', db.json())

    
    #2. Alter database
    db.change_marks()
    print('after mark change: ')
    db.print()

    #3. Convert db to bytes
    changed_bytes = db.get_bytes()       


    #4. encrypt with rsa
    changed_int = int.from_bytes(changed_bytes, byteorder='big')
    enc_msg_bytes = encrypt_rsa(changed_int, N, e)          #change it to N_client, and e_client BEFORE SUBMITTING


    
    #5. Hamming encode
    hamm_msg_bin = hamming_encode(enc_msg_bytes)
    hamm_msg_byte = bits_to_bytes(hamm_msg_bin)
    print("to send bytes:", hamm_msg_byte, len(hamm_msg_byte))

    
    #6. send to Arash's client
    
    print("header:", str(header) + str(hamm_msg_byte))
    print("")
    to_send = str(header) + str(hamm_msg_byte)

    request_bytes =  bytes(to_send, 'utf-8') 
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print ("Socket successfully created")
    except socket.error as err: 
        print ("socket creation failed with error %s" %(err))
    
    
    s.connect((HOST, PORT_client))
    s.send (request_bytes)
    
    #ready = select.select([s], [], [], 10)
    #if ready[0]:
    #    response = s.recv(64000)
    #    print("from arash after sending:", response)

    s.close()

    


    #VERIFICATION
    t_hamming = hamming_decode(hamm_msg_byte)
    t_hamming_int = int(t_hamming,2)
    t_decrypt = decrypt_rsa(t_hamming_int, N, d)
    print("Verify:", t_decrypt)
    





if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time)) # run time check