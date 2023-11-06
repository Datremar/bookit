from functools import wraps
from flask import request, jsonify
from models.token import Token

def login_required(func):
    @wraps(func)
    def log_req(*args, **kwargs):
        print(f"Middleware executed before {func.__name__}")
        try:
            authorization_header = request.headers.get('Authorization')
            if authorization_header is None:
                raise Exception(
                    "Authorization header is missing. " + 
                    "Please provide a valid token via Authorization: Bearer."
                )

            token = request.headers.get('Authorization').split()[1]
            my_token = Token.select_first(token=token)

            if my_token is None:
                raise Exception("Please provide a valid user token")
        except Exception as error:
            return jsonify({"error": str(error)}), 401

        return func(my_token['user_id'], *args, **kwargs)
    return log_req


def admin_required(func):
    @wraps(func)
    def sign_req(*args, **kwargs):
        print(f"Middleware executed before {func.__name__}")

        try:
            token = request.headers.get('Authorization').split()[1]
            # pylint: disable=line-too-long
            query = (
                "SELECT auth.id as 'user_id', token.`token`, auth.`role` as 'role' "
                "FROM token LEFT JOIN auth ON auth.id = token.user_id "
                "WHERE token = %s AND role = 'admin' "
                "LIMIT 1"
            )
            rows = Token.exec_query("".join(query), (token,))

            if not rows:
                raise Exception("Unautorized token")
            user_id = rows[0][0]
        except Exception as error:
            return jsonify({"error": str(error)}), 401

        return func(user_id, *args, **kwargs)
    return sign_req
