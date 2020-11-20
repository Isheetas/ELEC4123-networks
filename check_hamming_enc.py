from hamming import *


changed_bytes = b'dSc'


print("TESTING HAMMING ENCODE")
hamming_bin = hamming_encode(changed_bytes)
hamming_int = int(hamming_bin)
#print("len before decoding:",len(hamming_bin))

#print("decoding now")
test_hamm  =  hamming_decode(hamming_bin)
print("after decoding:", test_hamm, len(test_hamm))
print("after:", int(test_hamm, 2))

print("END OF TESTING HAMMING ENCODE")
print("")