from flask import Blueprint
from flask import request, jsonify
import pymysql
from assets.db import DatabaseTransaction

res_bp = Blueprint('response', __name__)


@res_bp.route('/add', methods=['POST'])
def add_res():
    try:
        data = request.get_json()
        if 'user_id' not in data.keys():
            return jsonify({"data":"user_id not found"})
        if 'form_id' not in data.keys():
            return jsonify({"data":"form_id not found"})
        if 'q_id' not in data.keys():
            return jsonify({"data":"q_id not found"})
        
        db = DatabaseTransaction()
        db.start_transaction()
        form_id = data.get("form_id")
        user_id = data.get("user_id")
        query = f"SELECT COUNT(*) FROM form WHERE form_id = {form_id} AND user_id = {user_id}"
        result = db.execute_query(query)
        if result[0][0] != 1:
            return {"data": "No such form exists"}

        q_id = data.get("q_id")
        query = f"SELECT COUNT(*) FROM question WHERE form_id = {form_id} AND q_id = {q_id}"
        result = db.execute_query(query)
        if result[0][0] != 1:
            return {"data": "No such question exists"}
    

        query=f"INSERT into response(qid,res_text) VALUES({data.get("q_id"),data.get("res_text")})"
        result = db.execute_query(query)
        db.commit_transaction()
        return jsonify({"data":result})
    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return jsonify({'data':error_message})


@res_bp.route('/update', methods=['POST'])
def update_res():
    try:
        data = request.get_json()
        if 'user_id' not in data.keys():
            return jsonify({"data":"user_id not found"})
        if 'form_id' not in data.keys():
            return jsonify({"data":"form_id not found"})
        if 'q_id' not in data.keys():
            return jsonify({"data":"q_id not found"})
        
        db = DatabaseTransaction()
        db.start_transaction()
        form_id = data.get("form_id")
        user_id = data.get("user_id")
        query = f"SELECT COUNT(*) FROM form WHERE form_id = {form_id} AND user_id = {user_id}"
        result = db.execute_query(query)
        if result[0][0] != 1:
            return {"data": "No such form exists"}

        q_id = data.get("q_id")
        query = f"SELECT COUNT(*) FROM question WHERE form_id = {form_id} AND q_id = {q_id}"
        result = db.execute_query(query)
        if result[0][0] != 1:
            return {"data": "No such question exists"}
    
        
        q_id = data.get("q_id")
        res_id = data.get("res_id")
        query = f"SELECT COUNT(*) FROM response WHERE res_id = {res_id} AND q_id = {q_id}"
        result = db.execute_query(query)
        if result[0][0] != 1:
            return {"data": "No such question exists"}
    

        query=f"UPDATE response SET res_text={data.get("res_text")} WHERE res_id = {res_id}"
        db.execute_query(query)
        db.commit_transaction()
        return jsonify({"data":"Resp updated"})
    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return jsonify({'data':error_message})


@res_bp.route('/delete', methods=['POST'])
def del_res():
    try:
        data = request.get_json()
        if 'user_id' not in data.keys():
            return jsonify({"data":"user_id not found"})
        if 'form_id' not in data.keys():
            return jsonify({"data":"form_id not found"})
        if 'q_id' not in data.keys():
            return jsonify({"data":"q_id not found"})
        
        db = DatabaseTransaction()
        db.start_transaction()
        form_id = data.get("form_id")
        user_id = data.get("user_id")
        query = f"SELECT COUNT(*) FROM form WHERE form_id = {form_id} AND user_id = {user_id}"
        result = db.execute_query(query)
        if result[0][0] != 1:
            return {"data": "No such form exists"}

        q_id = data.get("q_id")
        query = f"SELECT COUNT(*) FROM question WHERE form_id = {form_id} AND q_id = {q_id}"
        result = db.execute_query(query)
        if result[0][0] != 1:
            return {"data": "No such question exists"}
    
        
        q_id = data.get("q_id")
        res_id = data.get("res_id")
        query = f"SELECT COUNT(*) FROM response WHERE res_id = {res_id} AND q_id = {q_id}"
        result = db.execute_query(query)
        if result[0][0] != 1:
            return {"data": "No such question exists"}
    

        query=f"DELETE FROM response WHERE res_id = {res_id}"
        db.execute_query(query)
        db.commit_transaction()
        return jsonify({"data":"Response deleted"})
    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return jsonify({'data':error_message})

