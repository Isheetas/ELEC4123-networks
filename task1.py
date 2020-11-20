import socket
import select
import math
from type_conversions import bytes_to_bits, int_to_bytes
from rsa import decrypt_rsa
from hamming import hamming_decode


 
def main():
 
    # 1. Send well-formed HTTP requests
    HOST = '149.171.36.192'
    PORT = 12274
    host = '149.171.36.192' 

    #N = 63148583107154283585608284940392418734726981382069355868003882013090711003369
    #e = 65537
    #d = 51783437651169347215431900289402465246791119526563008636281618633074802696377
    N = 22946363129994826577290485132048269530367907435865564505398980418770939980335605558922215490228827703369553743626870315255204846515969276672521953249260400066138871749246384596075747255554938943120569769420923823686164862968767839306248417957032703462245871947555296177875829693435733439160109407765234856561636468093388251400122393226115460553654948341945632248422505234342191276574649191089998930866384791495629609740703256945567786500796606036156932805990473521378549032729928164863421133267054266084277047689600401729486564350762792635097639715603761556993068515886895509613259566547005980540352656342746261262537
    e = 65537
    d = 252792684740776428411488628795014275919337613389305851242779862708891445531567011208047966552408770646090266611205889308547200805415716583877212112943314598589381042814835736734465866892147426902864814891159299337800189680080723560417952572821118023402681226576360282594966950557099036316459261436754634731889905201747103851611449210570319678170771358908293749523108746287938161045351335725021400509975663317393973710483203568059596657971449782305265385988995877764594815999847585302822520276427822531443733852892804878775517133081958601862663391675487488874170650718742484619889643980014838982209372664534895730689




    content = str(N) + "," + str(e)
    print('content: ', content)
    # HTTP request headers
    request = 'GET / HTTP/1.1\r\nHost: ' + host + '\r\nContent-Length: ' + str(len(content)) + '\r\n\r\n' + content
    request_bytes =  bytes(request, 'utf-8') 
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print ("Socket successfully created")
    except socket.error as err: 
        print ("socket creation failed with error %s" %(err))
    
    
    s.connect((HOST, PORT))
    s.send (request_bytes)
    
    ready = select.select([s], [], [], 10)
    if ready[0]:
        response = s.recv(64000)
    #print(bytearray(data)) 
    
    #print(b'received msg: ' + response)
    response_tokens = response.split(b'\r\n\r\n')
    response_header = response_tokens[0] + b'\r\n\r\n'
    #print(b'response header:' + response_header)
    payload = response_tokens[1]
    print('bytes: ',len(payload))
 
    # extract output content - comes after \r\n\r\n
 
    # 2. Resolve hamming code on payload
    databits = bytes_to_bits(payload)       #makes payload into binary
    print('binary payload: ', databits, len(databits))

    corrected_databits = hamming_decode(payload)
    print('corrected: ', corrected_databits, ' ', len(corrected_databits))
  

    int_cipher = int(corrected_databits, 2)     #convert the bytes into an int, assumed big endian
    print('int_cipher: ', int_cipher)

    decrypted_payload = decrypt_rsa(int_cipher, N, d)
    print('dec: ', decrypted_payload)
    print('size: ', len(decrypted_payload))

    extract_marks(decrypted_payload)
    s.close()
 
def extract_marks(data):
    n_entries = data[0]

    print("n_entires: ", len(data))
    len_student_bytes = 10 # bytes taken up by each students information
    n = 0
    
    while n < n_entries:
        start = n*10 + 1
        # print(response[i]) 
        # first byte is number of students
        name = str(data[start:(start + 5)])
        t1 = data[start+5]
        t2 = data[start+6]
        t3 = data[start+7]
        t4 = data[start+8]
        total = data[start+9]
        print('name: ', name)
        print('t1:',  t1)
        print('t2:', t2)
        print('t3:', t3)
        print('t4:', t4)
        print('total:', total)
        n = n + 1
    
   


 
if __name__ == '__main__':
    main()
 
 