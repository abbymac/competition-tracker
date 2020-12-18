import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from decouple import config


AUTH0_DOMAIN = 'amack.us.auth0.com'
ALGORITHMS = config('ALGORITHMS')
API_AUDIENCE = config('API_AUDIENCE')


class AuthError(Exception):
    """ A standardized way to communicate auth failure modes
    Params:
        * error: description of error
        * status_code [type: int]: the HTTP status code
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """ get token header from auth header

    Params:
        * none

    - Checks if the auth header has exactly 2 parts.
      Looking for bearer and it's token.
        - If not 2 parts, raise 401 error
    - Checks if bearer token is present
        - If not present, raise 401 error
    """

    # check if authorization is in request header
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'no_authorization',
            'description': 'No authorization present in headers.'
        }, 401)

    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    # check for bearer token
    if len(header_parts) != 2:
        raise AuthError({
                'code': 'header_parts',
                'description': 'more or less than 2 parts in auth_header.'
            }, 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
                'code': 'no_bearer',
                'description': 'Bearer token not present.'
            }, 401)

    return header_parts[1]


def check_permissions(permission, payload):
    """ Checks to see if permissions are present in JWT
        Params:
            - permission [type: str]: Defines user's permission
                - example: get:drink-details
            - payload [type: dict]: The decoded JWT

        - Checks if permissions are present in payload
            - if not, raise 400 error
        - Checks if specific permission asked for is present
            - if not, raise 401 error
    """

    # checks if permissions field is present in payload
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT'
        }, 400)

    # checks if specific permission asked for is present
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permissions not found. Unauthorized.'
        }, 401)
    return True
    raise Exception('Not Implemented')


def verify_decode_jwt(token):
    """ Checks that jwt is valid and return decoded token in a dict
        Params:
            - token [type: str]: JWT passed from authentication

        - Raises [code#, code]:
            - [401, 'token_expired]: Token is expired
            - [401, 'invalid_claims]: Incorrect claims
            - [400, 'invalid_header]: unable to parse authentication token
            - [400, 'invalid_header]: Unable to find appropriate key

    """
    # get the public key from auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # get the data in header
    unverified_header = jwt.get_unverified_header(token)

    # get key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # use the key to validate the JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        # token is experpied
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        # user does not have valid claim
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': """Incorrect claims.
                Please check the audience and issuer."""
            }, 401)
        # token has error
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    """ Gets the access token, verifies and decodes token,
        then checks specific permissions

        - Params:
            - permission [type: str]: the permission to check token for.
              Defined by route
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
