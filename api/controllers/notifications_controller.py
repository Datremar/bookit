from flask_cors import cross_origin
from flask import request, jsonify, json
from middleware.auth import login_required, admin_required
from models.notifications import Notifications

# User actions
@cross_origin()
@login_required
def get_my_list(user_id: int) -> dict:
    """Fetch my notifications"""
    page = request.args.get('p', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    if limit > 50 and page > 0:
        return {'error': 'Limit must be less then 51 and page greater then 0'}

    offset = (page - 1) * limit
    notif_list = Notifications.select(
        limit=limit,
        offset=offset,
        order_by='created_at DESC',
        target_user_id = user_id
    )

    return jsonify(notif_list), 200

@cross_origin()
@login_required
def get_my_notif_details(user_id: int, notification_id: int) -> dict:
    """Get notification information"""
    notif_details = Notifications.select_first(
        target_user_id = user_id,
        id = notification_id
    )

    if notif_details is None:
        return {'error': "This user doesn't have this notification."}, 401

    return jsonify(notif_details), 200

@cross_origin()
@login_required
def ack(user_id: int, notification_id: int) -> dict:
    """Acknowledge notification"""
    Notifications.update(
        conditions={'id': notification_id, 'target_user_id': user_id},
        new_values={'ack': 1}
    )
    return {'status': 'OK'}, 201

# Admin actions
@cross_origin()
@admin_required
def get_all(_) -> dict:
    """Fetch all notifications"""
    page = request.args.get('p', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    if limit > 50 and page > 0:
        return {'error': 'Limit must be less then 51 and page greater then 0'}

    offset = (page - 1) * limit
    notif_list = Notifications.select(
        limit=limit,
        offset=offset,
        order_by='created_at DESC',
    )

    return jsonify(notif_list), 200

@cross_origin()
@admin_required
def get_notif_details(_, notification_id: int) -> dict:
    """Get notification information"""
    notif_details = Notifications.select_first(
        id = notification_id
    )

    if notif_details is None:
        return {'error': "Notification doesn't exist"}, 401

    return jsonify(notif_details), 200

@cross_origin()
@admin_required
def add_notification(_) -> dict:
    """Add new notification"""
    body = json.loads(request.data)

    try:
        new_notif = Notifications.insert(**body)
        return jsonify(new_notif), 201
    except Exception as e:
        return {'error': str(e)}

@cross_origin()
@admin_required
def update_notification(_, notification_id: int) -> dict:
    """Update notification info"""
    body = json.loads(request.data)

    try:
        Notifications.update(
            conditions={'id': notification_id},
            new_values=body
        )
        notif_update = Notifications.select_first(id=notification_id)
        return jsonify(notif_update), 200
    except Exception as e:
        return {'error': str(e)}

@cross_origin()
@admin_required
def del_notification(_, notification_id: int) -> dict:
    """Delete Notification"""
    Notifications.delete(conditions={'id': notification_id})
    return {'status': 'OK'}, 200
