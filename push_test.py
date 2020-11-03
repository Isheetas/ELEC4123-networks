#task 1 TELE3118 assignment
 
import socket
import select
 
# HOST = '149.171.36.192'
# PORT = 12274


# content = b'252837207378338387332619197259204540353,65537'
# request = b'GET / HTTP/1.1\r\nHost: 149.171.36.192\r\nContent-Length: 45\r\n\r\n' + content
# print(request)
 
# try: 
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#     print ("Socket successfully created")
# except socket.error as err: 
#     print ("socket creation failed with error %s" %(err))
 
# s.connect((HOST, PORT))
# s.send (request)
 
# ready = select.select([s], [], [], 10)
# if ready[0]:
#     data = s.recv(64000)
# print (data)

# 
# # data = data.decode('utf-8')
# print (data)
# s.close()

data = b'200 OK\r\nDate: Tue, 03 Nov 2020 12:57:17 AM GMT\r\nContent-Length: 18\r\n\r\n\x00\x8a\xbb\x1a%\x12\x11\xdb\xb6\x87\xa8\xf5>Es\x8f\xbd\x97'
headers = data[:(len(data) - 18)]
print(headers)