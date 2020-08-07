import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# define and assign API_AUDIENCE and AUTH0_DOMAIN and ALGORITHMS exported
# from setup.sh
AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.environ['ALGORITHMS']
API_AUDIENCE = os.environ['API_AUDIENCE']

# Defining AuthError Exception


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Getting the Auth Token Header
def get_token_auth_header():
    # get authorization header from request
    auth_header = request.headers.get('Authorization', None)
    # check if authoroization header exists
    if not auth_header:
        # raise auth error sice the authorization header is not present
        raise AuthError({
            'description': 'The Authorization header is not present.',
            'code': 'authorization_header_missing'
        }, 401)
    # split auth header into the bearer and token
    split_auth_header = auth_header.split()
    # check if the header sent is a bearer token
    if split_auth_header[0].lower() != 'bearer':
        # raise auth error since the authorization header is not a bearer token
        raise AuthError({
            'code': 'invalid_header',
            'description': 'The Authorization header must start with "Bearer".'
        }, 401)
    # Check if the split_auth_header array contains two items (bearer string
    # and token)
    elif len(split_auth_header) == 1:
        # if split_auth_header contain only 1 item ,raise auth error
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    # raise error if the split_auth_header contains more than two items, which
    # is invald and incorrect
    elif len(split_auth_header) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'The Authorization header must be a bearer token.'
        }, 401)

    # pass the second item in the split_auth_header array/dict whih is the
    # access token fron Auth0
    token = split_auth_header[1]
    return token


# Implementing function for checking and getting permission if exists
def check_permissions(permission, payload):
    # check if any permissions exist in the payload
    if 'permissions' not in payload:
        # raise Auth error since no permissions exists on the payload
        raise AuthError({
            'code': 'invalid per',
            'description': 'There are no Permssion not inlcuded in this payload'
        }, 401)
    # check if the permission sent is in the payload
    if permission not in payload['permissions']:
        # raise Auth error since there are no permissions in the permissions
        # array/dict
        raise AuthError({
            'code': 'unauthorized',
            'description': "You currently do not have permission to access this"
        }, 401)


# verifying the Decode JWT Token from Auth0
def verify_decode_jwt(token):
    # get jsonurl for Auth0 using Auth0 domain
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    # read and load the jsonurl
    jwks = json.loads(jsonurl.read())
    # verify token using the jose jwt library
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    # check if key id exists in the auth token
    if 'kid' not in unverified_header:
        # raise error if key id is not in header
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    # iterate through keys to get keys
    for key in jwks['keys']:
        # check if the kid exists
        if key['kid'] == unverified_header['kid']:
            # assign jwk keys to rsa_key dictionary
            rsa_key = {
                'kid': key['kid'],
                'kty': key['kty'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # check if RSA Key exists on the jwks dict
    if rsa_key:
        try:
            # decode using the jose jwt library
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload
        # raise Auth errors if expired token
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token has expired.'
            }, 401)
        # raise Auth error if claims is invalid
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        # raise error if error occured or function could not parse the
        # authentication token
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 401)
    # raise auth error if rsa_key does not exist
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 401)


# defining and implementing the require auth decorator
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # get access token from token header
            token = get_token_auth_header()
            # verify and decode jwt token
            payload = verify_decode_jwt(token)
            # check for permissions on the request  payload
            check_permissions(permission, payload)
            # return payload and decorator arguments
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
