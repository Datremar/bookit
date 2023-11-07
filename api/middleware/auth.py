from functools import wraps
from flask import jsonify
from models.token import Token
from services import token_service

def login_required(func):
    @wraps(func)
    def log_req(*args, **kwargs):
        print(f"Middleware executed before {func.__name__}")
        try:
            req_token = token_service.get_request_token()
            my_token = Token.select_first(token=req_token)

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
            req_token = token_service.get_request_token()
            # pylint: disable=line-too-long
            query = (
                "SELECT auth.id as 'user_id', token.`token`, auth.`role` as 'role' "
                "FROM token LEFT JOIN auth ON auth.id = token.user_id "
                "WHERE token = %s AND role = 'admin' "
                "LIMIT 1"
            )
            rows = Token.exec_query("".join(query), (req_token,))

            if not rows:
                raise Exception("Unautorized token")
            user_id = rows[0][0]
        except Exception as error:
            return jsonify({"error": str(error)}), 401

        return func(user_id, *args, **kwargs)
    return sign_req
