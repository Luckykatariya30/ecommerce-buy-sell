# pip install pycryptodome
import hashlib
import string
import random
import base64
from tkinter.messagebox import IGNORE
from Crypto.Cipher import AES

IV = '@@@@&&&&####$$$$'  # Initialization vector
BLOCK_SIZE = 16

def generate_checksum(param_dict, merchant_key, salt=None):
    params_string = get_param_string(param_dict)
    if salt is None:
        salt = generate_salt(4)
    final_string = f"{params_string}|{salt}"
    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()
    hash_string += salt
    
    return encrypt(hash_string, merchant_key)


def genereate_refund_checksum(param_dict, merchant_key, salt=None):
    params_string = get_param_string(param_dict)
    if salt is None:
        salt = generate_salt(4)
    final_string = f"{params_string}|{salt}"
    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()
    hash_string += salt
    
    return encrypt(hash_string, IV, merchant_key)



def generate_checksum_by_str(params_str, merchant_key, salt=None):
    if salt is None:
        salt = generate_salt(4)
    final_string = f"{params_str}|{salt}"
    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()
    hash_string += salt
    
    return encrypt(hash_string, IV, merchant_key)


def verify_checksum(param_dict, merchant_key, checksum):
    if 'CHECKSUMHASH' in param_dict:
        param_dict.pop('CHECKSUMHASH')
    #GET SALT
    paytm_hash = decrypt(checksum, IV, merchant_key)
    salt = paytm_hash[-4:]
    calculated_checksum = generate_checksum(param_dict, merchant_key, salt=salt)

    return calculated_checksum == checksum



def verify_checksum_by_str(params_str, merchant_key, checksum):
    paytm_hash = decrypt(checksum, IV, merchant_key)
    salt = paytm_hash[-4:]
    calculated_checksum = generate_checksum_by_str(params_str, merchant_key, salt=salt)

    return calculated_checksum == checksum

def verify_refund_checksum(param_dict, merchant_key, checksum):
    if 'CHECKSUMHASH' in param_dict:
        param_dict.pop('CHECKSUMHASH')
    #GET SALT
    paytm_hash = decrypt(checksum, IV, merchant_key)
    salt = paytm_hash[-4:]
    calculated_checksum = genereate_refund_checksum(param_dict, merchant_key, salt=salt)

    return calculated_checksum == checksum

def __id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_param_string(param_dict):
    params = sorted(param_dict.items())
    params_string = '|'.join(str(v) for k, v in params if v is not None and v != '')
    return params_string

def generate_salt(length):
    return __id_generator(size=length)  


def encrypt(input_string, key):
    key = key.encode('utf-8')
    input_string = pad(input_string).encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, IV.encode('utf-8'))
    encrypted = cipher.encrypt(input_string)
    encoded = base64.b64encode(encrypted).decode('utf-8')
    return encoded

def decrypt(encrypted_string, iv, key):
    key = key.encode('utf-8')
    encrypted_string = base64.b64decode(encrypted_string)
    cipher = AES.new(key, AES.MODE_CBC, iv.encode('utf-8'))
    decrypted = cipher.decrypt(encrypted_string).decode('utf-8')
    unpadded = unpad(decrypted)
    return unpadded

def pad(input_string):
    padding_length = BLOCK_SIZE - (len(input_string) % BLOCK_SIZE)
    padding = chr(padding_length) * padding_length
    return input_string + padding

def unpad(input_string):
    padding_length = ord(input_string[-1])
    return input_string[:-padding_length]


# --- IGNORE ---
if __name__ == "__main__":
    params = {
        'MID': 'YourMerchantID',
        'ORDER_ID': 'ORDER0001',
        'CUST_ID': 'CUST0001',
        'TXN_AMOUNT': '100.00',
        'CHANNEL_ID': 'WEB',
        'WEBSITE': 'WEBSTAGING',
        'INDUSTRY_TYPE_ID': 'Retail',
        'CALLBACK_URL': 'https://yourdomain.com/callback/',
    }
    merchant_key = 'YourMerchantKey'
    checksum = generate_checksum(params, merchant_key)
    print("Generated Checksum:", checksum)
    is_valid = verify_checksum(params, merchant_key, checksum)
    print("Is Checksum Valid?", is_valid)
   