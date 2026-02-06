from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"])

def hash_pass(password):
    return pwd.hash(password)

def verify_pass(password, hashed):
    return pwd.verify(password, hashed)