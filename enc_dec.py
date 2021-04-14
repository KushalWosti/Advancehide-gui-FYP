from base64 import b64encode, b64decode
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
import os
def encrypt(msg, enc_key):
    #generate a random salt
    salt = os.urandom(AES.block_size)
    # generate a random iv
    iv = Random.new().read(AES.block_size)
    # use the Scrypt KDF to get a private key from the password
    enc_secret_key = hashlib.scrypt(enc_key, salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    #Applying the padding to the secret message
    padded_text = pad(msg, AES.block_size)
    # create the cipher config
    enc_cipher = AES.new(enc_secret_key, AES.MODE_CBC, iv)
    # encrypt the message
    cipher_text = enc_cipher.encrypt(padded_text)
    #createing siction with item ic,Cipher_text and salt
    result = {'iv': b64encode(iv).decode(), 'ciphertext': b64encode(cipher_text).decode(), 'salt': b64encode(salt).decode()}
    return result
def decrypt(encrypted_dic,dec_key):
    #all the value here are in binary
    salt = b64decode(encrypted_dic['salt'].encode())
    enc_text = b64decode(encrypted_dic['ciphertext'].encode())
    iv = b64decode(encrypted_dic['iv'].encode())
    # generate the private key from the password and salt
    dec_secret_key = hashlib.scrypt(dec_key, salt=salt, n=2**14, r=8, p=1, dklen=32)
    # create the cipher config
    dec_cipher = AES.new(dec_secret_key, AES.MODE_CBC, iv)
    # decrypt the cipher text
    decrypted = dec_cipher.decrypt(enc_text)
    #Removing the padding that were added during the encryption process
    unpad_msg = unpad(decrypted, AES.block_size).decode()
    return unpad_msg
#original=decrypt(encrypted_dic,key)
#print(original)