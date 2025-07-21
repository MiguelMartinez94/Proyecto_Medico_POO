from flask import Blueprint, jsonify
from Cuerito import mysql

DBCheck_bp = Blueprint('DBCheck', __name__)

@DBCheck_bp.route('/DBCheck')
def DB_check():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT 1')
        return jsonify({'status': 'ok', 'message': 'Conectado con éxito'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
