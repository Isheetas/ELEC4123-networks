#client for extension task 1
import socket
from hamming_ext1 import *

#send request to task3_server
HOST = '127.0.0.1'
PORT = 3000
#host = 'localhost'

#request = 'GET / HTTP/1.1\r\nHost: ' + host + '\r\nContent-Length: ' + str(len(content)) + '\r\n\r\n' + content
request = 'thisisarequest'
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
#convert from bytes to bits
data = bytes_to_bits(data)
#split received data into blocks of size 8 bits
n = 8
splitresponse = [data[i:i + n] for i in range(0, len(data), n)]
#correct bit errors
hammingsplit = []
for x in splitresponse:
    hammingsplit.append(hamming_decode(x, 1))
print(hammingsplit)
#decoded = hamming_decode(data, 1)
#decoded = bits_to_bytes(decoded)
#display data
#print(decoded)