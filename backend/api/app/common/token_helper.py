import jwt
from datetime import datetime, timedelta
from ..database.UserModel import User
from flask import make_response, jsonify
from ..common.error_handling import Forbidden, Unauthorized


def generate_token(user_id, user_role):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'role': user_role
        }
        jwt_string = jwt.encode(
            payload,
            "supersecretkey",
            algorithm='HS256'
        )
        return jwt_string

    except Exception as e:
        return str(e)

def decode_token(token):
    try:
        payload = jwt.decode(token, "supersecretkey")
        return payload
    except jwt.ExpiredSignatureError:
        return "Expired token. Please login to get a new token"
    except jwt.InvalidTokenError:
        raise Unauthorized('prueba')

def validateToken(req, user_role):
    auth_header = req.headers.get('Authorization')
    if auth_header is None:
        raise Unauthorized('You have to be logged')
    access_token = auth_header.split(' ')[1]

    if access_token:
        payload = decode_token(access_token)
        if not isinstance(payload['sub'], str):
            if payload['role'] not in user_role:
                raise Forbidden('You are not allowed to access here')
            else:
                return payload['sub']
        else:
            message = user_id
            res = {
                'msg': message
            }
            return make_response(jsonify(res))
    else:
        raise Unauthorized('You have to be logged')