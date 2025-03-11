from dotenv import load_dotenv
import environ
import jwt
from datetime import datetime, timezone, timedelta
from rest_framework.exceptions import AuthenticationFailed
from core import settings
load_dotenv()
env = environ.Env()

class TokenManager:

    @staticmethod
    def generate_custom_token(data):
        payload = {
            'data': data,
            'exp': datetime.now(tz=timezone.utc) + timedelta(hours=1),
            'iat': datetime.now(tz=timezone.utc)
        }
        with open(settings.BASE_DIR.parent / "private_key.pem", 'r') as file:
            private_key = file.read()

        token = jwt.encode(payload, private_key, algorithm='RS256')
        
        return token
    
    @staticmethod
    def verify_custom_token(token):
        # try:
            
            with open(settings.BASE_DIR.parent / 'public_key.pem', 'r') as file:
                public_key = file.read()  
            payload = jwt.decode(token, public_key, algorithms=['RS256'])

            return payload
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('Token expirado.')
        # except jwt.InvalidTokenError:
        #     raise AuthenticationFailed('Token inválido.')