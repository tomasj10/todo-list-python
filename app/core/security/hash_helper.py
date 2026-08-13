from bcrypt import checkpw, hashpw, gensalt

UTF_METHOD = 'utf-8'

class HashHelper(object) :

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str): 
        # Checks if the plain password matches the hashed password
        if checkpw(plain_password.encode(UTF_METHOD), hashed_password.encode(UTF_METHOD)):
            return True
        return False

    @staticmethod
    def get_password_hash(plain_password: str):
        return hashpw(
            plain_password.encode(UTF_METHOD),
            gensalt()
        ).decode(UTF_METHOD)

    