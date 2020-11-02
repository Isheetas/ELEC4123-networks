#task 1 TELE3118 assignment
 
import socket
import select
 
HOST = '149.171.36.192'
PORT = 12274
 

message = "GET / HTTP/1.1\r\nContent-Length:128\r\nHost:149.171.36.192:12274\r\n252837207378338387332619197259204540353,65537\r\n"
messagebyte = message.encode('iso-8859-1')
#message = "GET / HTTP/1.1\r\n"
#parameters
'''
headers = """\
GET / HTTP/1.1\r
Content-Length: {content_length}\r
Host: {host}\r
Connection: close\r
\r\n"""

body = '252837207378338387332619197259204540353,65537'                                 
body_bytes = body.encode('ascii')
print(len (body_bytes))
header_bytes = headers.format(
    content_length=len(body_bytes),
    host=str(HOST) + ":" + str(PORT)
).encode('iso-8859-1')

payload = header_bytes + body_bytes
'''
message_byte = bytes(message, 'utf-8')
 
try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print ("Socket successfully created")
except socket.error as err: 
    print ("socket creation failed with error %s" %(err))
 
s.connect((HOST, PORT))
s.send (messagebyte)
 
#s.setblocking(0)
 
ready = select.select([s], [], [], 10)
if ready[0]:
    data = s.recv(64000)
print (data)
s.close()