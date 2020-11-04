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
    2. modify struct
    '''


    
    






    # struct student_data {
    #     char student_name[5];
    #     char mark_task1; // Max mark – 25
    #     char mark_task2; // Max mark - 15
    #     char mark_task3; // Max mark - 50
    #     char mark_task4; // Max mark - 10
    #     char mark_total; // Max mark - 100
    # }
    # struct database {
    #     char n_entries;
    #     student_data sample[n_entries];
    # }
    



    ''' 
    3. convert database structure to json serialisable object
    '''
    json_payload = json.dumps(payload.as_dict())
    print('json payload:' + json_payload)
    '''
    4. encrypt with rsa
    '''
    encrypted_payload = encrypt_rsa(json_payload, n, e)
    print('encrypted payload')
    print(encrypted_payload)
    
    # sanity check - decrypt payload
    decrypted_payload = pow(encrypted_payload, int(d), int(n))
    print('decrypted payload')
    print(decrypted_payload)
    decrypted_payload_bytes = decrypted_payload.to_bytes((decrypted_payload.bit_length() + 7) // 8, 'big')
    print(decrypted_payload_bytes)
    '''
    5. encode to hamming
    6. construct response and sent to user
    '''




'''
TBD: encrypt with rsa  
'''
def encrypt_rsa(payload, N, e):
    cipher = bytes(payload, 'utf-8')
    print('cipher:')
    print(cipher)
    int_cipher = int.from_bytes(cipher, byteorder='big')
    print('integer payload')
    print(int_cipher)
    # back to string
    # print('back to bytes')
    # cipher_to_bytes = int_cipher.to_bytes((int_cipher.bit_length() + 7) // 8, 'big')
    # print(cipher_to_bytes)
    return pow(int_cipher, int(e), int(N))

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