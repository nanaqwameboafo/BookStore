import jwt
from passlib.context import CryptContext
from datetime import timedelta,datetime, timezone
from src.config import Config
import uuid
import logging

password_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")
ASSESS_TOKEN_EXPIRE_MINUTES = 30
def Hash_password(plain_text:str) -> str:
    # Truncate password to 72 bytes as required by bcrypt
    hashed = password_context.hash(plain_text)
    return hashed


def verify_password(plain_text,hashed_password) -> bool:
    verify = password_context.verify(plain_text,hashed_password)
    return verify

def create_token(user_data:dict, expire_time:timedelta =None , refresh:bool = False) -> str:
    payload = {}
    payload['user'] = user_data
    # expiration: prefer provided expire_time, otherwise use a timezone-aware default
    payload['exp'] = (
        datetime.now(timezone.utc) + expire_time
        if expire_time is not None
        else datetime.now(timezone.utc) + timedelta(minutes=ASSESS_TOKEN_EXPIRE_MINUTES)
    )
    # include a JWT ID claim so other modules can identify tokens (depencies expects 'jti')
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    # token = jwt.encode(payload,Config.JWT_KEY,algorithm=Config.JWT_ALGORITHM)
    token = jwt.encode(
        payload = payload,
        key = Config.JWT_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token:str) -> dict:
    try:
        decoded_payload = jwt.decode(
            jwt = token,
            key = Config.JWT_KEY,
            algorithms = [Config.JWT_ALGORITHM]
        )
        return decoded_payload
    except jwt.DecodeError as e:
        logging.error(f"Token decoding error: {e}")
        return None
    except jwt.ExpiredSignatureError as e:
        logging.error(f"Token expired: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected token error: {e}")
        return None

    