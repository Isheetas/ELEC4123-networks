import socket
import select
import math
from TypeConversions import bytes_to_bits, int_to_bytes
from RSA import decrypt_rsa
from Hamming import hamming_decode
from Hamming import hamming_encode
HOST = '149.171.36.192'
PORT = 12002
host = '149.171.36.192' 

send_message = "hello world"


try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print ("Socket successfully created")
except socket.error as err: 
    print ("socket creation failed with error %s" %(err))

s.connect((HOST, PORT))
s.send (send_message.encode('utf-8'))
sendbit = bytes_to_bits (send_message.encode('utf-8'))
print ('send       ', sendbit)
ready = select.select([s], [], [], 10)
if ready[0]:
    response = s.recv(64000)
responsebit = bytes_to_bits (response)
print ('responsebit', responsebit)
n = 4
splitresponse = [responsebit[i:i+n] for i in range(0, len(responsebit), n)]
#intresponse = int (splitresponse,2)
#byteresponse = int_to_bytes(intresponse)
print ('splitresonse', splitresponse[1])
hammingsplit = []
i=0

while (i<len(splitresponse)):
    hammingsplit.append(hamming_encode (splitresponse[i],0))
    i=i+1
print ("hammingsplit", hammingsplit)
# need to concat with N,e

# decode
databits = bytes_to_bits(hammingsplit)
n=8
splitresponse = [databits[i:i+n] for i in range(0, len(databits), n)]
i=0
hammingsplitdecode = []
while (i<len(splitresponse)):
    hammingsplitdecode.append(hamming_decode (splitresponse[i],1))
    i=i+1
print ("hammingsplitdecode", hammingsplitdecode)

