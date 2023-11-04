from flask import jsonify
from flask_cors import cross_origin
import config

@cross_origin()
def index() -> dict:
    """Simple healthcheck with uptime info"""
    try:
        cursor = config.get_db_cursor()
        query = "show global status like 'Uptime'"
        cursor.execute(query)
        results = cursor.fetchall()
        return {'status': 'OK', 'uptime': int(results[0][1])}
    except Exception as e:
        config.close_db_con()
        return jsonify(
            {
                'status': 'ERROR',
                'message': 'Error during database operation',
                'db': f'{e}'}
        ), 500
