import hashlib
from models.auth import Auth
from models.token import Token
import config

def create_token(username: str) -> str:
    """
    Create token
    
    :returns: token
    :raises Exception: if not valid username
    """
    user = Auth.select_first(username=username)

    if user is None:
        raise Exception("Username does not exist")

    return create_token_by_user_id(user[id])

def create_token_by_user_id(user_id: int) -> str:
    """
    Create token
    
    :returns: token
    :raises Exception: if not valid user_id
    """
    my_token = config.generate_token()
    Token.insert(
        user_id=user_id,
        token=my_token
    )
    return my_token

def hash_pass(password: str) -> str:
    """ Hash users password """
    return hashlib.sha256(password.encode()).hexdigest()
