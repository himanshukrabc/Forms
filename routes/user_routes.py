from flask import Blueprint
from flask import request, jsonify
import pymysql
from assets.db import DatabaseTransaction

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def reg_user():
    try:
        data = request.get_json()
        db = DatabaseTransaction()
        db.start_transaction()
        if 'username' in data.keys():
            username = data.get('username')
            query = f"SELECT COUNT(*) FROM user WHERE username = '{username}'"
            result = db.execute_query(query)[0][0]
            print(result)
            if(result == 0):
                query = f"INSERT INTO user(username) VALUES ('{username}')"
                result = db.execute_query(query,True)
            else:
                result='username not unique'
        else:
            result='username not added'
        db.commit_transaction()
        return jsonify({'data': result})

    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return jsonify({'data':error_message})


@user_bp.route('/get', methods=['POST'])
def get_user():
    try:
        data = request.get_json()
        db = DatabaseTransaction()
        db.start_transaction()
        if 'user_id' in data.keys():
            user_id = data.get('user_id')
            query = f"SELECT * FROM user WHERE user_id = '{user_id}'"
            result = db.execute_query(query)
        else:
            result='user_id/username not added'
        db.commit_transaction()
    
        return jsonify({'data': result})
    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return jsonify({'data':error_message})


@user_bp.route('/delete', methods=['POST'])
def del_user():
    try:
        data = request.get_json()
        db = DatabaseTransaction()
        db.start_transaction()
        if 'user_id' in data.keys():
            user_id = data.get('user_id')
            query = f"DELETE FROM user WHERE user_id = '{user_id}'"
            db.execute_query(query)
            result='user deleted'
        else:
            result='user_id/username not added'
        db.commit_transaction()
        return jsonify({'data': result})
    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return jsonify({'data':error_message})
