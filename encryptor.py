from cryptography.fernet import Fernet

def load_key():
    return open("secret.key", "rb").read()

def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    return f.decrypt(encrypted_message.encode()).decode()
