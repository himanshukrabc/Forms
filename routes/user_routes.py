from flask import Blueprint
from flask import request, jsonify
import pymysql
from assets.db import execute_query

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def reg_user():
    try:
        data = request.get_json()
        if 'username' in data.keys():
            username = data.get('username')
            query = f"SELECT COUNT(*) FROM user WHERE username = '{username}'"
            result = execute_query(query)[0][0]
            print(result)
            if(result == 0):
                query = f"INSERT INTO user(username) VALUES ('{username}')"
                result = execute_query(query,True)
                return jsonify({'data': result})
            else:
                return jsonify({'data': 'username not unique'})
        else:
            return jsonify({'data': 'username not added'})
    
    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return {'data':error_message}\


@user_bp.route('/get', methods=['POST'])
def get_user():
    try:
        data = request.get_json()
        if 'user_id' in data.keys():
            user_id = data.get('user_id')
            query = f"SELECT * FROM user WHERE user_id = '{user_id}'"
            result = execute_query(query)
            return jsonify({'data': result})
        else:
            return jsonify({'data': 'user_id/username not added'})
    
    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return {'data':error_message}


@user_bp.route('/delete', methods=['POST'])
def del_user():
    try:
        data = request.get_json()
        if 'user_id' in data.keys():
            user_id = data.get('user_id')
            query = f"DELETE FROM user WHERE user_id = '{user_id}'"
            execute_query(query)
            return jsonify({'data': 'user deleted'})
        else:
            return jsonify({'data': 'user_id/username not added'})
    
    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return {'data':error_message}
