# add YOUR implementation for the three functions
# do NOT modify code outside of the functions
from crypto_utils import get_string_hash
from crypto_utils import CryptoTool
import os

PASSWORDS_FILE = "users.data"
USER_NAME = "bob"
MESSAGES_FILE = f"messages_{USER_NAME}.data"


def _read_user_hash(password_file_name, u_name):
    '''
    input: name of file with user data (e.g., users.data)
    input: required username (e.g., "bob")
    return hash of the user's password as stored in the user file,
        this hash should be returned as a string (e.g., "2c89060719a95c7cb741f04e36835430436840e3052273676c6c1a99")
    return None in case of any issues,
        e.g., file not found or user not found
    '''
    # ... your code here ...
    if password_file_name in os.listdir():
        file = open(password_file_name, "r")
        for lines in file.readlines():
            info = lines.strip().split(",")
            
        if info[0] == u_name:
            return info[1]          # return password hash
        else:
            return "user not found"
    else:
        return "file not found"

def _guess_password(h):
    '''
    input: hash of a password as a string
    return a four digit password as a string (e.g., "0123")
        such that hash for this password matches the input hash
    return None if no such password found
    '''
    # ... your code here ...
    i = 0000
    while i < 10000:
        if get_string_hash(str(i)) == h:
            return str(i)
        i += 1

def _recover_message(messages_file_name, password):
    '''
    input: name of file with encrypted user messages
    input: user password in plain text
    return the first message as a string
    return None in case of any issues,
        e.g., no messages, file not found, etc.
    '''
    # ... your code here ...
    if messages_file_name in os.listdir():
        file = open(messages_file_name, "rb")
        for info in file.readlines():
            # decrypt the message
            decrypt_password = CryptoTool(password)
            decrypt_messages = decrypt_password.decrypt(info)
            
            # return first message
            for message in decrypt_messages:
                return message
    
    
if __name__ == "__main__":
    h = _read_user_hash(PASSWORDS_FILE, USER_NAME)
    password = _guess_password(h)
    message = _recover_message(MESSAGES_FILE, password)
    
    print(h)
    print(password)
    print(message)
    