# add YOUR implementation for the three functions
# do NOT modify code outside of the functions
from crypto_utils import get_string_hash
from crypto_utils import CryptoTool


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

def _guess_password(h):
    '''
    input: hash of a password as a string
    return a four digit password as a string (e.g., "0123")
        such that hash for this password matches the input hash
    return None if no such password found
    '''
    # ... your code here ...

def _recover_message(messages_file_name, password):
    '''
    input: name of file with encrypted user messages
    input: user password in plain text
    return the first message as a string
    return None in case of any issues,
        e.g., no messages, file not found, etc.
    '''
    # ... your code here ...

if __name__ == "__main__":
    h = _read_user_hash(PASSWORDS_FILE, USER_NAME)
    password = _guess_password(h)
    message = _recover_message(MESSAGES_FILE, password)
    
    print(h)
    print(password)
    print(message)
    