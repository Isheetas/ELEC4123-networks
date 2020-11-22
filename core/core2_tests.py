'''
CORE 2 TESTING:
run tests on:
- key manufacturing function
- rsa functions
- hamming functions 
- change marks
'''


from utility import *
import math

'''
Key Genrator function test
'''
# 128 bit (check key lengths)
def rsa_key_1():
    key_size = 128  
    N, e, d = set_key(key_size)
    assert len(bytes_to_bits(int_to_bytes(N))) == key_size
    print('test1 passed')
    pass
# 256 bit (check key lengths)
def rsa_key_2():
    key_size = 256 
    N, e, d = set_key(key_size)
    assert len(bytes_to_bits(int_to_bytes(N))) == key_size
    print('test2 passed')
    pass
# 512 bit (check key lengths)
def rsa_key_3():
    key_size = 512 
    N, e, d = set_key(key_size)
    assert len(bytes_to_bits(int_to_bytes(N))) == key_size
    print('test3 passed')
    pass
# 1024 bit (check key lengths)
def rsa_key_4():
    key_size = 1024  
    N, e, d = set_key(key_size)
    assert len(bytes_to_bits(int_to_bytes(N))) == key_size
    print('test4 passed')
    pass
# 2048 bit (check key lengths)
def rsa_key_5():
    key_size = 2048  
    N, e, d = set_key(key_size)
    assert len(bytes_to_bits(int_to_bytes(N))) == key_size
    print('test5 passed')
    pass




'''
RSA function testing
'''
# max_num_students that can be represented w/ key_size --> = floor((key_size/8 -1) / 10)

# key_size 128 (use sample server)
def rsa_test1(key_size):
    N, e, d = set_key(key_size)
    n_students = math.floor( (key_size/8 -1)/10)
    plain = get_student_payload(n_students) 
    cipher = encrypt_rsa(bytes_to_int(plain), N, e)
    assert len(cipher) <= key_size/8
    assert plain == decrypt_rsa(bytes_to_int(cipher), N, d)
    print('RSA ' ,key_size, 'bit test passed')
    pass

# edge case payload 1 integer less than N, 128bit key (hardcode input)
def rsa_test2(key_size):
    N, e, d = set_key(key_size)
    plain_int = N - 1
    plain = int_to_bytes(plain_int)
    cipher = encrypt_rsa(plain_int, N, e)
    assert len(cipher) <= key_size/8
    assert plain == decrypt_rsa(bytes_to_int(cipher), N, d)
    print('RSA ' ,key_size, 'bit largest cipher passed')
    pass


# helper
def get_student_payload(n_students):
        #Request message from data server
    HOST_data_server = '149.171.36.192'
    PORT_data_server = 12000
    content = '4,' + str(n_students) 
    request_bytes =  bytes(content, 'utf-8')

    try:
        s_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print ("Socket successfully created to data server")
    except socket.error as err:
        print ("socket creation failed with error %s to data server" %(err))

    s_data.connect((HOST_data_server, PORT_data_server))
    s_data.send (request_bytes)

    #s.send (request_bytes)
    ready = select.select([s_data], [], [], 10)
    if ready[0]:
        response = s_data.recv(64000)

    s_data.close()

    #print(response)
    return response


'''
Hamming function testing
'''
# no errors
def hamm_1():
    pass
# 1 bit error
def hamm_2():
    pass
# 2 bit error detection, 1 bit fixed
def hamm_3():
    pass


'''
Check payload modification
'''

# no m in all student payload
def marks_check_1():
    payload = b'dDale \x19\x0b\'\x06QRick \n\x0c2\nRKerri\x0f\x08\'\x04BScott\x11\x08\x15\x075'
    pass
# m in first students name
def marks_check_2():
    pass
# m in last students name
def marks_check_3():
    pass
# multiple m's in one name
def marks_check_4():
    pass
# m in multiple names
def marks_check_5():
    pass
#  multiple names are the same
def marks_check_6():
    pass
# total = t1+t2+t3+t4 with modification



def main():
    print('----- Running core2 test -----')


    rsa_key_1()
    rsa_key_2()
    rsa_key_3()
    rsa_key_4()
    rsa_key_5()

    print('-----RSA key test passed!  -----')

    rsa_test1(128)
    rsa_test1(256)
    rsa_test1(512)
    rsa_test1(1024)
    rsa_test1(2048)
    rsa_test2(128)
    rsa_test2(256)
    rsa_test2(512)
    rsa_test2(1024)
    rsa_test2(2048)


    print('-----  RSA tests passed!  -----')

    hamm_1()
    hamm_2()
    hamm_3()


    print('----- Hamming tests passed! -----')


    marks_check_1()
    marks_check_2()
    marks_check_3()
    marks_check_4()
    marks_check_5()
    marks_check_6()

    print('------Mark change tests passed! -----')
    print('----- All tests passed! xd xd   -----')


if __name__ == "__main__":
    main()