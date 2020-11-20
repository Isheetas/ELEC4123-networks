import socket
import select
import json
import struct
import time

def main():
    # these values will be recieved from client
    n = '252837207378338387332619197259204540353'
    e = '65537'
    d = '48393883292703003300067554859838128129'

    HOST_server = '149.171.36.192'
    PORT_d = 12000

    content = '4,100'
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
        plaintext = s_data.recv(64000)

    s_data.close()

    print("resp: ", plaintext)
    print(" ")

    #key_size = '128'

    #print(int(d))

    #plaintext = b'dScott\x10\n\'\x04ESara \r\t\x1c\x068John \x0c\t\x15\x071Brian\x11\n#\x04BJamie\x0f\x0c0\x08SGlenn\x19\t"\x06JAdam \x0f\x0c\x10\x061Dana \x12\x07%\x04BWayne\x12\x07#\x06BSara \x15\t"\x08HMolly\x10\r*\x06MJohn \r\t\'\nGLance\x0c\x0b&\x04AMary \r\x0b\x1d\x049Omar \x0f\t"\x07ALance\x0f\r&\x07IHenry\x14\x0c\x18\x06>Judy \x10\x07&\x08ELisa \x13\x0c\x19\x06>Aimee\x0f\x08,\x05HTanya\x13\t2\x07UKyle \x11\n+\x03ILynn \x19\r\x1f\x07LAna  \x0f\x0c#\x06DJason\x10\r\'\x06JTraci\x10\n)\x06IBobby\x12\x06\x1a\x08:Dana \x0b\x0c\x1b\x079Lisa \x0c\r\x16\x076Judy \x0e\t+\x07IMandy\x0c\n \n@Robin\x14\x0c2\t[Laura\r\x0c2\x06QKevin\x10\x0c(\x06JWanda\x12\x05"\x08ALinda\x0c\x0c!\tBTracy\x0e\n \x08@James\x19\x0c\'\x08TCarla\x11\x042\x04KTodd \x12\x08\'\x06GTony \x17\x0c\x17\x06@Jamie\r\r!\x04?Ana  \x0f\t\x0b\x04\'James\x13\t.\x04NLinda\x0c\x0c!\tBLisa \x19\t,\x05SDawn \x12\x08\x0e\x07/Henry\x19\n,\x06UAaron\x10\x08+\tLBrian\x0b\n\x1a\x065Toni \x17\n)\x08RIan  \x0b\t)\x04ABrian\x12\x0f#\x05IMason\x13\x08\x12\x074James\x0e\t*\x04ELaura\x0c\n$\x07AJesse\x18\n.\x08XJenny\x18\t\x16\x06=Brian\x11\x0e+\x07QToni \x11\r0\x05SMegan\t\x0e.\x05JDavid\x0e\x0b\x1d\x028Tammy\x0e\x0c)\x06ITim  \r\n-\x06JLori \x14\n)\x08OBrian\x13\x0f#\x05JWayne\x12\x07#\x06BTracy\x10\x0c"\tGRyan \r\t2\tQEric \x11\x0c\x1f\x08DSean \x12\t)\x07KRyan \x13\x0b\x1b\x05>Kayla\x12\t\x1e\x06?Kevin\x18\n$\nPRyan \x0e\x0f*\x04KCathy\x07\x080\x04CJon  \x0c\t$\x06?Megan\x11\x08*\x08KDonna\x13\x0b \nHColin\x16\n\x1a\x06@Edwin\x11\t(\tKPaige\x0e\x061\x04ITina \x07\x05\x17\x06)Lance\x0f\r&\x07IDonna\x0e\x0f\x1e\x06ADiana\x11\n\x0e\x05.April\x15\n%\x06JCindy\x0b\x08\x19\x073Terri\x0e\x0b1\x07QChad \x0e\n-\nOTina \x13\x0c1\nZJulia\x10\x08\x19\x034Adam \x10\t(\x07HErica\x18\n\x1c\x06DLori \x10\x07\x1a\x067Kyle \x0b\x0e+\x07KTraci\x10\n)\x06ITina \x13\x0e\x0f\x066Shawn\x0f\x0b\x13\x052Shawn\r\x05#\x05:'


    print('input length:', len(plaintext))
    print('plaintext', plaintext)
    #encrypted_payload = encrypt_rsa(plaintext, n, e)

    encrypted_payload_full = encrypt_rsa(plaintext, n, e)
    print('full encrypted:', encrypted_payload_full )
    decrypted_payload_full = decrypt_rsa(encrypted_payload_full, n, d)
    print('full load:', decrypted_payload_full)


def encrypt_rsa(msg_bytes, n, e):
    '''
    Encrypt with RSA 
    Input plaintext (String e.g 'Hello') - payload to encrypt as a text string, n(String), e(String)
    Output cipher_bytes (String e.g  b'\xa9z\xb7\xf3\')
    '''
    cipher_bytes_temp = b''
    cipher_bytes = b''
    start = 0
    while start < len(msg_bytes):
        end = start + 16
        msg_int = int.from_bytes(msg_bytes[start:end], byteorder='big')
        cipher_int = pow(msg_int, int(e), int(n))
        cipher_bytes_temp = int_to_bytes(cipher_int)
        cipher_bytes = cipher_bytes + cipher_bytes_temp
        start = end
    return cipher_bytes



def decrypt_rsa(cipher_bytes, n, d):
    # message to decrypt will always be a multiple of 16
    plaintext_bytes_temp = b''
    plaintext_bytes = b''
    start = 0
    while start < len(cipher_bytes):    
        end = start + 16
        cipher_int = int.from_bytes(cipher_bytes[start:end], byteorder='big') # convert cipher to integer form
        plaintext_int = pow(cipher_int, int(d), int(n))
        plaintext_bytes_temp = int_to_bytes(plaintext_int)
        plaintext_bytes = plaintext_bytes + plaintext_bytes_temp
        start = end
    return plaintext_bytes


def int_to_bytes(integer_val):
    '''
    input: int
    output: list of bytes(binary) 
    '''
    return integer_val.to_bytes((integer_val.bit_length() + 7) // 8, 'big')




if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time)) # run time check