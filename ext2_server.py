# create server and client
import socket
import select
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


def main():
    #CREATE SERVER
    HOST = '127.0.0.1'
    PORT = 3000
    HOST_server = '149.171.36.192'
    PORT_d = 12000


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((HOST, PORT))
    s.listen(5)

    conn, addr = s.accept()
    print(f"Connection from {addr} has been established.")

    # while True:
    #
    #     try:
    #         data = conn.recv(1024)
    #
    #         if not data: break
    #         print("Client says: ")
    #         print(data)
    #         #conn.close()
    #
    #     except socket.error:
    #         print ("Error Occured.")
    #         break

    data = conn.recv(1024)

    #Request message from data server
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
        response = s_data.recv(64000)

    s_data.close()

    print(response)

    #encrypt with rsa

    # data = str(data)
    # #payload = data.split('b')
    # payload_split = data.split(',')
    # n = int(payload_split[0])
    # e = int(payload_split[1])
    # encrypt_rsa(response, n, e)

    payload = str(data)
    payload = payload[2:len(payload)-1]
    payload_split = payload.split(',')
    n = int(payload_split[0])
    print(n)
    e = int(payload_split[1])
    print(e)
    cipher = encrypt_rsa(response, n, e)
    print(cipher)

    #send noisy payload to client
    conn.sendall(cipher)


if __name__ == '__main__':
    main()
 