from flask import Blueprint
from controllers import auth_controller as ctl

auth_blueprint = Blueprint('auth', __name__)

# user commands
auth_blueprint.route('/login', methods=['POST'])(ctl.get_my_token)
auth_blueprint.route('/token', methods=['DELETE'])(ctl.revoke_my_token)
auth_blueprint.route('/', methods=['GET'])(ctl.get_my_data)
auth_blueprint.route('/', methods=['PUT'])(ctl.update_my_data)
auth_blueprint.route('/', methods=['DELETE'])(ctl.close_my_account)

# admin other users
auth_blueprint.route('/manage/list', methods=['GET'])(ctl.get_users_list)
auth_blueprint.route('/manage/<int:user_id>', methods=['GET'])(ctl.get_data)
auth_blueprint.route('/manage', methods=['POST'])(ctl.add_user)
auth_blueprint.route('/manage/<int:user_id>', methods=['PUT'])(ctl.update_data)
auth_blueprint.route(
    '/manage/<int:user_id>',
    methods=['DELETE']
)(ctl.close_account)
