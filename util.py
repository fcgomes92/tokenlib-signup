import hashlib

def set_password(password):
    m = hashlib.sha256(password.encode('ascii')).hexdigest()
    return m
