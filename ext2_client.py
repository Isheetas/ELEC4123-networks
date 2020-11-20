#client for extension task 1
import socket

#send request to task3_server
HOST = '127.0.0.1'
PORT = 3000
#host = 'localhost'

#request = 'GET / HTTP/1.1\r\nHost: ' + host + '\r\nContent-Length: ' + str(len(content)) + '\r\n\r\n' + content
#client sends 'n,e'
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
#correct bit errors

#remove error correcting codes

#display data