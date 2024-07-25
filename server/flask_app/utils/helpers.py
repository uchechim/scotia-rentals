#used to store utility functions that are used across different parts of the application.

#I.E: Hash Password, Generate Random Id, Format API Response e.t.c

import hashlib
import random

def hash_password(password):
    sha256_password = hashlib.sha256(password.encode())
    encrypted_user_password = sha256_password.hexdigest()

    return encrypted_user_password


#reference -> https://stackoverflow.com/questions/72926478/how-do-you-auto-generate-a-random-id-for-an-sqlite-database-table
def generate_random_id():
    return random.randint(10000000, 99999999)#generates random 8 digit number

'''
3 functions to be used in app later
def format_response(message, status_code, data=None):
    response = {
        'message': message
    }
    if data:
        response['data'] = data
    return make_response(jsonify(response), status_code)

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def get_config_var(name, default=None):
    return os.getenv(name, default)
'''