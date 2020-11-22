import socket
import select
import json
import struct
from utility import *
from type_conversions import *
import time



'''
TASK 2

'''


def main():

    
    HOST = '149.171.36.192'
    PORT_client = 12275
    PORT_db = 12274    

    '''
    0. Get request from Arash's client
    '''
    try: 
        s_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print ("Socket successfully created to Arash")
    except socket.error as err: 
        print ("socket creation failed with error %s to Arash" %(err))
    s_client.connect((HOST, PORT_client))

    ready = select.select([s_client], [], [], 10)
    if ready[0]:
        response = s_client.recv(64000)
        #print('request from arash client: ', response) 

    s_client.close


    '''
    1. Extract Arash client keys
    '''
    client_request = split_http_message(response)
    client_content = client_request['content']
    client_keys = client_content.split(b',')
    N_client = int(client_keys[0])
    e_client = int(client_keys[1])

    


    '''
    2. Send request to Demo db with OUR set key and get message
    '''
    key_size = len(str(bin(N_client))) -2  # our key-size should be the same as key-size sent by arash client
    N, e, d = set_key(key_size)            # retrieve local public and private RSA keys
    db_response = get_data_from_db(HOST, PORT_db, N, e, d)
    msg = db_response['content']
    header = db_response['header']

    '''
    3. Resolve hamming on payload from demo db
    '''
    corrected_msg = hamming_decode(msg)
    corrected_msg = int(corrected_msg, 2)

    '''
    4. Decrypt message from demo db with private RSA key
    '''
    decrypt_msg = decrypt_rsa(corrected_msg, N, d)


    '''
    1. Store DB content locally, alter student marks & display it
    '''
    db = create_db(decrypt_msg) # create DB class
    print('Before mark modification')
    db.print() 
    db.change_marks()
    print('After mark modification')
    db.print()

          

    '''
    3. Encrypt modified payload with RSA
    '''
    changed_bytes = db.get_bytes()  # convert db to bytes
    changed_int = bytes_to_int(changed_bytes)
    enc_msg_bytes = encrypt_rsa(changed_int, N_client, e_client)


    '''
    4. Encode with hamming
    '''
    hamm_msg_bin = hamming_encode(enc_msg_bytes)
    hamm_msg_byte = bits_to_bytes(hamm_msg_bin)

    
    '''
    5. Send response to Arash's client
    '''
    response_bytes = header + hamm_msg_byte # form request message

    # add in 5. if needed
        #print(response_bytes)
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print ("Socket successfully created")
    except socket.error as err: 
        print ("socket creation failed with error %s" %(err))
    
    
    s.connect((HOST, PORT_client))
    s.send (response_bytes)
    s.close()

    #s_client.send (response_bytes)
    #s_client.close



if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time)) # run time check






    # add in 5. if needed
        #print(response_bytes)
    # try: 
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #     print ("Socket successfully created")
    # except socket.error as err: 
    #     print ("socket creation failed with error %s" %(err))
    
    
    # s.connect((HOST, PORT_client))
    # s.send (response_bytes)
    # s.close()


    #VERIFICATION
    # t_hamming = hamming_decode(hamm_msg_byte)
    # t_hamming_int = int(t_hamming,2)
    # t_decrypt = decrypt_rsa(t_hamming_int, N, d)
    # print("Verify:", t_decrypt)