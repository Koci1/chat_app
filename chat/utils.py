import random
import string

def generate_username():
    randomString = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase,k=8))
    return f'User_{randomString}'