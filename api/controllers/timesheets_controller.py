import json
from flask_cors import cross_origin
from flask import request
from pydantic.json import pydantic_encoder
from middleware.auth import login_required, admin_required
from models.timesheets import Timesheets

# User actions
@cross_origin()
@login_required
def list_my_timesheets(user_id: int, item_id: int) -> dict:
    """Fetch my TimeSheets"""
    # TODO: Build this function
    return {'status': 'OK', 'user': user_id, 'timesheet': item_id}, 200

@cross_origin()
@login_required
def get_my_timesheet(user_id: int, item_id: int) -> dict:
    """Get Timesheet information"""
    # TODO: Build this function
    return {'status': 'OK', 'user': user_id, 'timesheet': item_id}, 200

@cross_origin()
@login_required
def create_my_timesheet(user_id: int) -> dict:
    """Create new Timesheet"""
    # TODO: Build this function
    return {'status': 'OK', 'user': user_id}, 200

@cross_origin()
@login_required
def update_my_timesheet(user_id: int, item_id: int) -> dict:
    """Update Timesheet data"""
    # TODO: Build this function
    return {'status': 'OK', 'user': user_id, 'timesheet': item_id}, 200

@cross_origin()
@login_required
def delete_my_timesheet(user_id: int, item_id: int) -> dict:
    """Remove Timesheet"""
    # TODO: Build this function
    return {'status': 'OK', 'user': user_id, 'timesheet': item_id}, 200

@cross_origin()
@login_required
def set_status(user_id: int, item_id: int) -> dict:
    """Set Timesheet status"""
    # TODO: Build this function
    return {'status': 'OK', 'user': user_id, 'timesheet': item_id}, 200

# Admin actions
@cross_origin()
@admin_required
def list_timesheets(_) -> dict:
    """Fetch all Timesheets"""
    page = request.args.get('p', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    if limit > 50 and page > 0:
        return {'error': 'Limit must be less then 51 and page greater then 0'}

    offset = (page - 1) * limit
    users_list = Timesheets.select(
        limit=limit,
        offset=offset,
        order_by='created_at DESC'
    )
    return json.dumps(users_list, default=pydantic_encoder), 200

@cross_origin()
@admin_required
def get_timesheet(_, item_id: int) -> dict:
    """Get Timesheet information"""
    # TODO: Build this function
    return {'status': 'OK', 'id': item_id}, 200

@cross_origin()
@admin_required
def create_timesheet(_) -> dict:
    """Create new Timesheet"""
    # TODO: Build this function
    return {'status': 'OK'}, 201

@cross_origin()
@admin_required
def update_timesheet(_, item_id: int) -> dict:
    """Update Timesheet data"""
    # TODO: Build this function
    return {'status': 'OK', 'id': item_id}, 200

@cross_origin()
@admin_required
def delete_timesheet(_, item_id: int) -> dict:
    """Remove Timesheet"""
    # TODO: Build this function
    return {'status': 'OK', 'user': item_id}, 201
