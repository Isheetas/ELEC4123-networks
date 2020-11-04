import socket
import select
import json
import struct
def main():
    # these values will be recieved from client
    n = '252837207378338387332619197259204540353'
    e = '65537'
    d = '48393883292703003300067554859838128129'
    print(int(d))

    '''
    0. get request from client
    '''

    '''
    1. get a json serialisable object
    '''
    payload = Database()
    payload.add_student(Student('Jason', '20', '10', '30', '10', '70'))
    payload.add_student(Student('Jack', '5', '5', '20', '10', '40'))
    payload.add_student(Student('Jane', '10', '10', '10', '10', '40'))
    payload.add_student(Student('John', '25', '10', '40', '10', '85'))


    '''
    2. Alter payload struct
    '''
    
    ''' 
    3. convert database structure to json serialisable object
    '''
    json_payload = json.dumps(payload.as_dict())
    print('json payload:' + json_payload)
    '''
    4. encrypt with rsa
    '''
    plaintext = "Hello"
    print(plaintext)
    encrypted_payload = encrypt_rsa(plaintext, n, e)
    print(encrypted_payload)
    decrypted_payload = decrypt_rsa(encrypted_payload, n, d)
    print(decrypted_payload)

    '''
    5. encode to hamming
    '''

    '''
    6. construct response and sent to user
    '''




'''
Encrypt with RSA 
Input plaintext (String e.g 'Hello') - payload to encrypt as a text string, n(String), e(String)
Output cipher_bytes (String e.g  b'\xa9z\xb7\xf3\')
'''
def encrypt_rsa(plaintext, n, e):
    plaintext_int = int.from_bytes(bytes(plaintext, 'utf-8'), byteorder='big') # convert plaintext to integer form
    cipher_int = pow(plaintext_int, int(e), int(n))
    cipher_bytes = cipher_int.to_bytes((cipher_int.bit_length() + 7) // 8, 'big')
    # cipher = str(cipher_bytes, 'utf-8')
    return cipher_bytes


'''
Decrypt with RSA
Input cipher (Byte String e.g. b'\xa9z\xb7\xf3\') - payload to decrypt as a text string, n(String), d(String)
Output plaintext (String e.g 'Hello')
'''
def decrypt_rsa(cipher_bytes, n, d):
    cipher_int = int.from_bytes(cipher_bytes, byteorder='big') # convert cipher to integer form
    plaintext_int = pow(cipher_int, int(d), int(n))
    plaintext_bytes = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big')
    plaintext = str(plaintext_bytes, 'utf-8')
    return plaintext




'''
TBD: decode with hamming
'''
def hamming_decode(byte_string):
    return 0



'''
TBD: encode with hamming
'''
def hamming_encode(byte_string):
    return 0


'''
CLASS DEFINITIONS
'''


class Database:
    def __init__(self):
        self.n_entries = 0
        self.sample = list()

    def add_student(self, student):
        self.sample.append(student)
        self.n_entries += 1

    def as_dict(self):
        student_dict = list()
        for student in self.sample:
            student_dict.append(student.as_dict())

        return {
            "n_entries": self.n_entries,
            "sample": student_dict,
        }
    


class Student:
    def __init__(self, name, mark_task1, mark_task2, mark_task3, mark_task4, mark_total):
        self.student_name= name
        self.mark_task1 = mark_task1
        self.mark_task2 = mark_task2
        self.mark_task3 = mark_task3
        self.mark_task4 = mark_task4
        self.mark_total = mark_total 

    def as_dict(self):
        return {
            "student_name": self.student_name,
            "mark_task1": self.mark_task1,
            "mark_task2": self.mark_task2,
            "mark_task3": self.mark_task3,
            "mark_task4": self.mark_task4,
            "mark_total": self.mark_total
        }
    



if __name__ == '__main__':
    main()