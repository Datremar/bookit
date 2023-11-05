from flask import Blueprint
from controllers import timesheets_controller as ctl

blueprint = Blueprint('timesheets', __name__)

# user commands
blueprint.route('/list', methods=['GET'])(ctl.list_my_timesheets)
blueprint.route('/<int:item_id>', methods=['GET'])(ctl.get_my_timesheet)
blueprint.route('/', methods=['POST'])(ctl.create_my_timesheet)
blueprint.route('/<int:item_id>', methods=['PUT'])(ctl.update_my_timesheet)
blueprint.route('/<int:item_id>', methods=['DELETE'])(ctl.delete_my_timesheet)
blueprint.route('/status/<int:item_id>', methods=['POST'])(ctl.set_status)

# admin other users
blueprint.route('/manage/list', methods=['GET'])(ctl.list_timesheets)
blueprint.route('/manage/<int:item_id>', methods=['GET'])(ctl.get_timesheet)
blueprint.route('/manage/', methods=['POST'])(ctl.create_timesheet)
blueprint.route('/manage/<int:item_id>', methods=['PUT'])(ctl.update_timesheet)
blueprint.route(
    '/manage/<int:item_id>',
    methods=['DELETE']
)(ctl.delete_timesheet)
