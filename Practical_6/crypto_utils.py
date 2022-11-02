'''
Do NOT modify this file
You need to install Python cryptography module for this to work
Use the following command to install: pip install cryptography

While you are welcome to explore this file, you do NOT need
to understand it for the purposes of the practical
'''
import base64
import hashlib
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_string_hash(s):
    return hashlib.sha224(s.encode()).hexdigest()
    
    
class CryptoTool:
    # encryption/decryption will be specific to the password
    # (encryption/decryption key will be based on the password)
    def __init__(self, password):
        # derive a symmetric key based on user's password
        # this key will be used to encrypt and decrypt messages
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=bytes(0), iterations=10000)
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.frenet = Fernet(key)
        
    # input: Python data structure, e.g., a list of strings
    # output: array of bytes with encrypted data
    def encrypt(self, data):
        # convert messages from list of strings to a string
        data_string = json.dumps(data)
        # then convert the string to a bytestream
        data_bytes = data_string.encode()
        # encrypt the bytestream
        cypher = self.frenet.encrypt(data_bytes)
        return cypher
        
    # input: encrypted array of bytes
    # output: decrypted data, e.g., Python list
    def decrypt(self, cypher):
        # decrypt data into a bytestream
        data_bytes = self.frenet.decrypt(cypher)
        # convert bytestream to a string
        data_string = data_bytes.decode()
        # convert the string to a list of strings
        data = json.loads(data_string)
        return data
