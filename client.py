import socket

import logging

UDP_IP = '149.171.37.161'
UDP_PORT = 5000

message = 'studentmarklist' + '\0'
message_byte = bytes(message,'utf-8')

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
	#print("connecting to server")
	s.sendto(message_byte, (UDP_IP,UDP_PORT))
	#print("sending message: " + str(message_byte) + " to the server")
	#print('recieving message from server')
	data, addr = s.recvfrom(1024)
	data = data.decode()
	students = []
	names = []
	marks = []
	#print(str(data))
	numstudents = int(data[slice(4)])
	i = 0
	for i in range(numstudents):
		name = data[slice(20*i+4,20*i+20,1)].rstrip("\0")
		mark = int(data[slice(20*i+20,20*i+24,1)])

		names.append(name)
		marks.append(mark)


	s.close()

