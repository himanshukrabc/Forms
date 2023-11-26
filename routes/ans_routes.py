from flask import Blueprint
from flask import request, jsonify
import pymysql
from assets.db import DatabaseTransaction
from assets.sheets import insert_answer

ans_bp = Blueprint('answer', __name__)

@ans_bp.route('/add', methods=['POST'])
def add_ans():
    try:
        data = request.get_json()
        if 'form_id' not in data.keys():
            return jsonify({"data":"form_id not found"})
        
        db = DatabaseTransaction()
        db.start_transaction()
        form_id = data.get("form_id")
        query = f"SELECT spreadsheetId FROM form WHERE form_id = {form_id}"
        result = db.execute_query(query)
        if len(result[0]) != 1:
            return jsonify({"data": "No such form exists"})
        spreadsheetId=result[0][0]
        ans_id_list = []
        ans_list = []
        for ans in data.get('answers'):
            qid = ans.get("qid")
            if "response_id" in ans.keys():
                query = f"INSERT INTO answer_mcq(q_id,res_id,user_id) VALUES {qid,ans.get("response_id"),data.get("user_id")}"
                ans_list.append(ans.get("response_id"))
            else:
                query = f"INSERT INTO answer_text(q_id,ans_text,user_id) VALUES {qid,ans.get("ans_text"),data.get("user_id")}"
                ans_list.append(ans.get("ans_text"))
            ans_id_list.append(db.execute_query(query,True))
        db.commit_transaction()

        insert_answer(spreadsheetId,data.get("user_id"),ans_list)
        return jsonify({"data":ans_id_list})
    
    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return jsonify({'data':error_message})

