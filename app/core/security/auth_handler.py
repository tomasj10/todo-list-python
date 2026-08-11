import jwt
import time

from app.core.config import JWT_ALGORITHM, JWT_SECRET

class AuthHandler(object): 
    @staticmethod
    def sign_jwt(user_email: str) -> str :
        payload = {
            "user_email" : user_email,
            "expires" : time.time() + 1800 # 30 minutes from now
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    @staticmethod
    def decode_jwt(token : str) -> dict : 
        try: 
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

            return decoded_token if decoded_token['expires'] >= time.time() else None
        except: 
            print('Unable to decode this token')

