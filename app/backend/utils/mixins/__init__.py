import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def get_random_email(length):
    random_string = f'{get_random_string(length)}.com'
    half_length = int(round(length/2,0))
    result_str = f'{random_string[:half_length]}@{random_string[half_length:]}'
    return result_str
