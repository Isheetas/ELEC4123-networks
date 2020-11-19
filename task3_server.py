# create server and client
import socket
import select

#CREATE SERVER
HOST = '127.0.0.1'
PORT = 3000
HOST_server = '149.171.36.192'
PORT_d = 12000
PORT_n = 12002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(5)

conn, addr = s.accept()
print(f"Connection from {addr} has been established.")

#Request message from data server
content = '4,3'
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

#encode with hamming

#INSERT HAMMING CODE HEREEEEEEEEEEEE!!!

#send bytes to noise server
try:
    s_noise = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created to noise server")
except socket.error as err:
    print ("socket creation failed with error %s to noise server" %(err))

s_noise.connect((HOST_server, PORT_n))
s_noise.send (response)

ready_noise = select.select([s_noise], [], [], 10)
if ready_noise[0]:
    noiseResponse = s_noise.recv(64000)

s_noise.close()

print(noiseResponse)

#send noisy payload to client
conn.sendall(noiseResponse)



