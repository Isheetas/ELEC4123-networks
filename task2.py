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
    #N = 119484048255701441436361811740544499805482989972762171328000832460793482937842746490520045389267019914879180293493128527411951756175646012207372245640392613181330180655929701724130504407998065166504932760922418859359543355490102783596328490356612554010085829097705629454807851698735754870179265036374094717849
    #e = 65537
    #d = 98169554028663195074268552344192732906999665503049451108954221656222986744450928903192736378388878867457838199542716308146908681554447642908863140933908360961506320097008245680412967700092994045241465985522036307059609765358467340869704010033821712100383554558800942218221868532481354259885666372749501435361

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

    print("n:", N_client)
    print("e:", e_client)




    '''
    0. send request to client (db?) and get message
    '''

    
    # return message header for future use as we
    response = get_data_from_db(HOST, PORT_db, N, e, d)
    msg = response.get_content()
    msg_bin = bytes_to_bits(msg)
    # msg_bin = convert_payload_binary(msg)
    corrected_msg = hamming_decode(msg_bin)
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
    #db.change_marks()
    #print('after: ', db.json())

    '''
    3. Convert db to bytes
    '''
    changed_bytes = db.get_bytes()

    '''
    4. Hamming encode
    '''
    #hamming_bin = hamming_encode(changed_bytes)
    #hamming_int = int(hamming_bin)

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