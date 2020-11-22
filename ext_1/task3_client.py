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
#s.close()
print('Received', repr(data))
#convert from bytes to bits
data = bytes_to_bits(data)
#print(data)
#split received data into blocks of size 8 bits
n = 8
splitresponse = [data[i:i + n] for i in range(0, len(data), n)]
#print(splitresponse)
#correct bit errors
hammingsplit = []
resendFlag = 0
for x in splitresponse:
    binDecoded = hamming_decode(x, 1)
    hammingsplit.append(binDecoded)
    if binDecoded == 'resend':
        print(x)
        print("NEED TO RESEND")
        resendFlag = 1

#print(hammingsplit)
if resendFlag == 1:
    request_again = 'resend'
    request_again_bytes = bytes(request_again, 'utf-8')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))

    s.connect((HOST, PORT))
    s.send(request_again_bytes)

    data_again = s.recv(1024)
    s.close()
    print('Received', repr(data_again)) #same data w new noise
    data_again = bytes_to_bits(data_again)
    splitresponse_again_ = [data_again[i:i + n] for i in range(0, len(data_again), n)]
    hammingsplit_again = []
    #assuming won't need to be resent a third time
    for x in splitresponse_again_:
        binDecoded = hamming_decode(x, 1)
        hammingsplit_again.append(binDecoded)

    #compare both received messages
s.close()
strOutput = ""
out = strOutput.join(hammingsplit)

decoded = bits_to_bytes(out)
#decoded = hamming_decode(data, 1)
#decoded = bits_to_bytes(decoded)
#display data
print(decoded)