from flask import request

def get_request_token() -> str:
    """
    Get token from request header.
    
    :returns: token string or None if token is not found.
    """
    authorization_header = request.headers.get('Authorization')
    if authorization_header is None:
        return None

    authorization = authorization_header.split()
    if len(authorization) < 2:
        return None

    return authorization[1]
