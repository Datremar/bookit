from flask import Blueprint
from controllers import notifications_controller as ctl

notif_blueprint = Blueprint('notifications', __name__)

# user commands
notif_blueprint.route('/list',
                      methods=['GET'])(ctl.get_my_list)
notif_blueprint.route('/<int:notification_id>',
                      methods=['GET'])(ctl.get_my_notif_details)
notif_blueprint.route('/ack/<int:notification_id>',
                      methods=['POST'])(ctl.ack)

# admin other users
notif_blueprint.route('/manage/list',
                      methods=['GET'])(ctl.get_all)
notif_blueprint.route('/manage/<int:notification_id>',
                      methods=['GET'])(ctl.get_notif_details)
notif_blueprint.route('/manage',
                      methods=['POST'])(ctl.add_notification)
notif_blueprint.route('/manage/<int:notification_id>',
                      methods=['PUT'])(ctl.update_notification)
notif_blueprint.route('/manage/<int:notification_id>',
    methods=['DELETE'])(ctl.del_notification)
