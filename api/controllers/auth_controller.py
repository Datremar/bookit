from flask_cors import cross_origin
from flask import request, jsonify, json
from middleware.auth import login_required, admin_required
from models.auth import Auth
from models.token import Token
from services import auth_service

# User actions
@cross_origin()
def get_my_token() -> dict:
    """Generate token for a user"""
    data = json.loads(request.data)

    if not data or 'username' not in data or 'password' not in data:
        return {'error': 'Invalid request body'}, 400

    hashed_password = auth_service.hash_pass(data['password'])

    user = Auth.select_first(username=data['username'], password=hashed_password)

    if user is None:
        return {'error': 'Username or password are invalid'}, 401

    user_token = auth_service.create_token_by_user_id(user['id'])
    return {'token': user_token}, 200

@cross_origin()
@login_required
def revoke_my_token(_) -> dict:
    """Delete token for user"""
    token = request.headers.get('Authorization').split()[1]
    Token.delete(token=token)
    return {'status': 'OK'}, 200

@cross_origin()
@login_required
def get_my_data(user_id: int) -> dict:
    """Fetch user_id data"""
    user = Auth.select_first(id=user_id)
    return jsonify(user), 200

@cross_origin()
@login_required
def update_my_data(user_id: int) -> dict:
    """Change values for user_id"""
    # TODO: Change user data from database
    return {'status': 'OK', 'user_id': user_id}

@cross_origin()
@login_required
def close_my_account(user_id: int) -> dict:
    """Make user_id inactive"""
    Auth.update(conditions={'id': user_id}, new_values={'active': 0})
    Token.delete(conditions={'user_id': user_id})
    return {'status': 'OK', 'user_id': user_id}

# Admin actions
@cross_origin()
@admin_required
def get_data(_, user_id: int) -> dict:
    """Fetch user_id data"""
    user = Auth.select_first(id=user_id)
    return jsonify(user), 200

@admin_required
def get_users_list(_) -> dict:
    """Fetch user_id data"""
    page = request.args.get('p', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    if limit > 50 and page > 0:
        return {'error': 'Limit must be less then 51 and page greater then 0'}

    offset = (page - 1) * limit
    users_list = Auth.select(
        limit=limit,
        offset=offset,
        order_by='created_at DESC'
    )
    return jsonify(users_list), 200

@cross_origin()
@admin_required
def add_user(_) -> dict:
    """Fetch user_id data"""
    # TODO: add new user to db based on json body data
    return {'status': 'OK'}

@cross_origin()
@login_required
def update_data(_, user_id: int) -> dict:
    """Change values for user_id"""
    # TODO: Change user data from database
    return {'status': 'OK', 'user_id': user_id}

@cross_origin()
@login_required
def close_account(_, user_id:int) -> dict:
    """Make user_id inactive"""
    Auth.update(conditions={'id': user_id}, new_values={'active': 0})
    Token.delete(conditions={'user_id': user_id})
    return {'status': 'OK', 'user_id': user_id}
