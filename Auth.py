import os
from hashlib import pbkdf2_hmac
import Crypto
from Crypto.PublicKey import RSA
import Crypto.Random
# https://nitratine.net/blog/post/how-to-hash-passwords-in-python/#why-not-use-sha-256-or-something-similar
import jwt
import Database


def encryptedPassword(password, salt):
    return pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        200000  # It is recommended to use at least 100,000 iterations of SHA-256
    )

def generateSalt():
    return Crypto.Random.get_random_bytes(32)

def verifyPassword(password_to_check, email):
    salt= Database.getSaltFromStorage(email)
    print('salt:')
    print(salt)

    key = Database.getPasswordFromStorage(email)
    new_key = encryptedPassword(password_to_check, salt)
    print(new_key==key)
    return new_key==key

def generateTokenRSA(email):
    key = generateAndStoreKeys(email)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    print(str(public_key).strip())
    encoded = jwt.encode({"email": email, "public_key ": str(public_key)}, private_key, algorithm="RS256")
    return encoded


def generateToken(email):
    # secret = Crypto.Random.get_random_bytes(32)
    secret = '123456789'
    Database.storeSecret(secret, email)
    encoded = jwt.encode({"email": email}, secret, algorithm="HS256")
    return encoded

def generateAndStoreKeys(email):
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    Database.storeSecrets(private_key,public_key, email)
    return key


def verifyToken(token,secret):
    print(jwt.decode(token,secret, algorithms="HS256"))


if __name__ == '__main__':
    print(jwt.decode('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InBoaWxpcHAuZ3JpbGxAZnJlZW5ldC5kZSJ9.bZIZ3mtbEwLRxJfZUZLjiflxrpYna3jQzWFpYzTqeZI','123456789', algorithms="HS256"))