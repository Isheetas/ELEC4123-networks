#task 1 TELE3118 assignment

import socket

HOST = '149.171.37.161'
PORT = 5000

message = "studentmarklist\0"
message_byte = bytes(message, 'utf-8')

print("1. Creating socket")
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    print("2. Connecting to the server")
    s.connect((HOST, PORT))
    print("3. Sending message: " + str(message_byte) + " to the server")
    s.sendall(message_byte)
    print("4. Receiving message from the server")
    data = s.recv(1024)

    print('      Received:', repr(data))
    print("5. Closing the socket")
    s.close()

