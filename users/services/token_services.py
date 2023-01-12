import datetime as dt
import jwt
from config import settings

def generate_access_token(user):
    access_token_payload = {
        'user_id': user.id,
        'exp': dt.datetime.utcnow() + dt.timedelta(days=0, minutes=600),
        'iat': dt.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token

def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': dt.datetime.utcnow() + dt.timedelta(days=1),
        'iat': dt.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token
