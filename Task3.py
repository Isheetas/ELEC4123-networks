import socket
import select
import math
from rsa import encrypt_rsa, decrypt_rsa
from type_conversions import bytes_to_bits, int_to_bytes, bits_to_bytes, bytes_to_int
from rsa import decrypt_rsa
from hamming import hamming_decode
from hamming import hamming_encode
HOST = '149.171.36.192'
PORT = 12002
host = '149.171.36.192' 
# implement server stuff here



'''
try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #print ("Socket successfully created")
except socket.error as err: 
    #print ("socket creation failed with error %s" %(err))
#sending data to noise function
s.connect((HOST, PORT))
s.send (send_message.encode('utf-8'))
sendbit = bytes_to_bits (send_message.encode('utf-8'))
#print ('send       ', sendbit)
ready = select.select([s], [], [], 10)
if ready[0]:
    response = s.recv(64000)
responsebit = bytes_to_bits (response)
#print ('responsebit', responsebit)
'''
responsebit = '0000000011111111'
n = 4
splitresponse = [responsebit[i:i+n] for i in range(0, len(responsebit), n)]
#intresponse = int (splitresponse,2)
#byteresponse = int_to_bytes(intresponse)
print ('splitresonse', splitresponse)
hammingsplit = []
i=0
N = 63148583107154283585608284940392418734726981382069355868003882013090711003369
e = 65537
d = 51783437651169347215431900289402465246791119526563008636281618633074802696377

while (i<len(splitresponse)):
    hammingsplit.append(hamming_encode (splitresponse[i],1))
    i=i+1
#print ("hammingsplit", hammingsplit) #P bit is leftmost
hammingsplitint = int(''.join(hammingsplit),2)
#print ('hammingsplitint',hammingsplitint)
sendoff = encrypt_rsa (hammingsplitint, N, e)
try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print ("Socket successfully created")
except socket.error as err: 
    print ("socket creation failed with error %s" %(err))
#sending data to noise function
s.connect((HOST, PORT))
s.send ((sendoff))
print (' sendoff', bytes_to_bits(sendoff))
ready = select.select([s], [], [], 10)
if ready[0]:
    response = s.recv(64000)
print ('response', bytes_to_bits(response))

receive = response
receiveint = bytes_to_int (receive)
receivedecrypt = decrypt_rsa (receiveint, N, d)
# receive decrypt has waaay too many bits
print ('receivedecrypt',bytes_to_bits(receivedecrypt))
##print ('receivedecrypt',receivedecrypt)
decryptbin = bytes_to_bits(receivedecrypt)
n = 8
decryptbinsplit = [decryptbin[i:i+n] for i in range(0, len(decryptbin), n)]
#print ("decryptbinsplit", decryptbinsplit)
hammingsplitdecode = []
i=0
while (i<len(decryptbinsplit)):
    hammingsplitdecode.append(hamming_decode (decryptbinsplit[i],1))
    i=i+1
print ("hammingsplitdecode", hammingsplitdecode)
