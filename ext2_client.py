#client for extension task 1
import socket
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



#send request to task3_server
HOST = '127.0.0.1'
PORT = 3000
#host = 'localhost'

#request = 'GET / HTTP/1.1\r\nHost: ' + host + '\r\nContent-Length: ' + str(len(content)) + '\r\n\r\n' + content
#client sends 'n,e'
n = '252837207378338387332619197259204540353'
d = '48393883292703003300067554859838128129'
request = '252837207378338387332619197259204540353,65537'
request_bytes = bytes(request, 'utf-8')
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
except socket.error as err:
    print("socket creation failed with error %s" % (err))

s.connect((HOST, PORT))
s.send(request_bytes)

data = s.recv(1024)
s.close()
print('Received', repr(data))

#decrypt data
plaintext = decrypt_rsa(data, n, d)

#display data
print(plaintext)