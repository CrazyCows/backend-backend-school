import bcrypt

class Encryption:
    def hash_password(self, password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed, salt

    def verify_password(self, stored_hash, password: str):
        password_bytes = password.encode('utf-8')
        if bcrypt.checkpw(password_bytes, stored_hash):
            return True
        else:
            return False
