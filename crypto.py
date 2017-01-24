import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

#iv: initialization vector

def md5(data):
    import hashlib
    return hashlib.md5(data).digest()

def cipher(key, iv):
    key = md5(key) #normalize key to 128 bits
    return Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())


def encrypt(key, iv, data):
    """ encrypts data by AES.CFB
    key :: bytestring
    iv :: bytestring[16]
    data :: bytestring[16*n]
    returns bytestring[16*n]"""

    enc = cipher(key, iv).encryptor()
    return enc.update(data) + enc.finalize()

def decrypt(key, iv, data):
    """ decrypts AES.CFB data
    key :: bytestring
    iv :: bytestring[16]
    data :: bytestring[16*n]
    returns bytestring[16*n]"""

    dec = cipher(key, iv).decryptor()
    return dec.update(data) + dec.finalize()


#these 2 methods manage iv on top of endec
def ivencrypt(key, data):
    iv = os.urandom(16)
    return iv + encrypt(key, iv, data)

def ivdecrypt(key, data):
    iv = data[:16]
    data = data[16:]
    return decrypt(key, iv, data)


def spitb(name, data):
    with open(name, 'wb') as f:
        f.write(data)

def slurpb(name):
    with open(name, 'rb') as f:
        return f.read()

#this padding will be permanent, but is not a problem for .json
def pad16(data):
    """pads data with trailing spaces, 
    so length is multiple of 16"""
    return data + (b' ' * (len(data) % 16))


def file_encrypt(key, fname, aesname=None):
    if aesname is None:
        aesname = fname + '.aes'

    data = ivencrypt(key, pad16(slurpb(fname)))
    spitb(aesname, data)

def file_decrypt(key, fname, aesname=None):
    if aesname is None:
        aesname = fname + '.aes'

    data = ivdecrypt(key, slurpb(aesname))
    spitb(fname, data)

