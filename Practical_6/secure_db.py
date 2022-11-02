# 1. implement _is_strong_password() function
# 2. fix the problem as described in instructions
import os

from crypto_utils import get_string_hash
from crypto_utils import CryptoTool
from getpass import getpass


PASSWORDS_FILE = "users.data"
MESSAGE_FILE_PREFIX = "messages_"


#############################################################
# below are some auxiliary functions
#############################################################

def _get_messages_file_name(u_name):
    return f"{MESSAGE_FILE_PREFIX}{u_name}.data"
    
def _enter_new_username(user_info):
    while True:
        u_name = input("Enter new username > ")
        if u_name in user_info:
            print("Username already exists.")
            continue
        if not u_name.isalnum():
            print("Only alphanumeric characters are allowed.")
            continue
        return u_name
        
    return None
    
def _enter_new_password():
    while True:
        p1 = getpass(prompt="Enter a new password > ")
        p2 = getpass(prompt="Type the same password again > ")
        if p1 == p2:
            if _is_strong_password(p1):
                print("Good, that's a strong password.")
            else:
                print("WARNING: your password is weak.")
            return p1
        print("Passwords do not match, try again.")

    return None

def _is_strong_password(password):
    '''
    input: password as a Python string
    return True if the password is strong, False otherwise
    
    A password is considered strong if ALL of these apply:
    - it is at least 8 characters long
    - it has at least one lowercase letter and at least one uppercase letter
    - it contains at least one digit
    - it contains at least one of these three special characters: $, @, #
    '''
    # ... your code here ...
    return False  # <-- remove this line if you don't need it

#############################################################
# below are functions that deal with user accounts
#############################################################

def _create_root_account():
    print("No root account detected.")
    print("You need to create root password.")
    u_hash = _enter_new_password()
    with open(PASSWORDS_FILE, 'w') as f:
        f.write(f"root,{u_hash}\n")
    print("Root account has been created.")

def _load_user_info():
    user_info = {}
    with open(PASSWORDS_FILE, 'r') as f:
        for line in f:
            tokens = line.rstrip().split(",")
            u_name = tokens[0]
            u_hash = tokens[1]
            assert u_name not in user_info, f"Repeated user {u_name}"
            user_info[u_name] = u_hash
            
    return user_info

def _attempt_login(user_info):
    u_name = input("Enter your username > ")
    u_pass = getpass(prompt="Enter your password > ")
    if u_name not in user_info:
        return None, None
    
    entered_hash = u_pass
    stored_hash = user_info[u_name]
    
    if entered_hash != stored_hash:
        return None, None
        
    return u_name, u_pass

def _work_with_user_list(user_info):
    print("You have been recognised as root.")
    while True:
        print("Enter command: (l)ist users, (a)dd a user, or (e)xit.")
        command = input("root> ").lower()
        if command == 'l':
            _print_user_names(user_info)
        elif command == 'a':
            _create_user_account(user_info)
        elif command == 'e':
            break

def _print_user_names(user_info):
    print("-" * 30)
    for u_name in user_info.keys():
        print(u_name)
    print("-" * 30)
    print()
    
def _create_user_account(user_info):
    u_name = _enter_new_username(user_info)
    u_hash = _enter_new_password()
    with open(PASSWORDS_FILE, 'a') as f:
        f.write(f"{u_name},{u_hash}\n")
    user_info[u_name] = u_hash
    print("Account has been created.")
    print()

#############################################################
# below are functions that deal with messages
#############################################################

def _work_with_messages(u_name, u_pass):
    print(f"Hello, {u_name}!")
    messages = _load_user_messages(u_name, u_pass)
    
    while True:
        print("Enter command: (l)ist messages, (a)dd a message, or (e)xit.")
        command = input(f"{u_name}> ").lower()
        if command == 'l':
            _print_messages(messages)
        elif command == 'a':
            _add_user_message(u_name, messages)
            _save_user_messages(u_name, u_pass, messages)
        elif command == 'e':
            break

def _load_user_messages(u_name, u_pass):
    message_file = _get_messages_file_name(u_name)
    if not os.path.isfile(message_file):
        return []
        
    messages = []
    with open(message_file, 'rb') as f:
        # read encrypted data from file
        cypher = f.read()
        c_tool = CryptoTool(u_pass)
        messages = c_tool.decrypt(cypher)
        
    return messages

def _save_user_messages(u_name, u_pass, messages):
    message_file = _get_messages_file_name(u_name)
    with open(message_file, 'wb') as f:
        # encrypt message list and save to file
        c_tool = CryptoTool(u_pass)
        cypher = c_tool.encrypt(messages)
        f.write(cypher)

def _print_messages(messages):
    print("-" * 30)
    for message in messages:
        print(message)
    print("-" * 30)
    print()

def _add_user_message(u_name, messages):
    print("Enter a message.")
    message = input(f"{u_name}> ")    
    messages.append(message)
    print("Message added.")
    print()
    
#############################################################
# below is the main program
#############################################################

if __name__ == "__main__":
    if not os.path.isfile(PASSWORDS_FILE):
        # if this is the first time to run the program,
        # create root password first
        _create_root_account()
    
    # this is a dictionary where each user name
    # is mapped to password (hash) of that user
    user_info = _load_user_info()
    
    # in case of failed login, keep trying again and again
    while True:
        u_name, u_pass = _attempt_login(user_info)
        if u_name is not None:
            # login was successful, leave the loop
            break
        print("Incorrect credentials. Try again.")
        
    if u_name == "root":
        # root cannot store messages
        # root can only add new users
        _work_with_user_list(user_info)
    else:
        # an authenticated user can store messages
        _work_with_messages(u_name, u_pass)
    