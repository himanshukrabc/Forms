from flask import Blueprint
from flask import request, jsonify
import pymysql
from assets.db import DatabaseTransaction
from assets.sheets import del_ques,upd_ques,insert_ques
ques_bp = Blueprint("ques", __name__)

@ques_bp.route("/add", methods=["POST"])
def add_ques():
    try:
        data = request.get_json()

        if "user_id" not in data.keys():
            return jsonify({"data": "user_id/username not added"})
        if "form_id" not in data.keys():
            return jsonify({"data": "form_id not added"})

        db = DatabaseTransaction()
        db.start_transaction()

        form_id = data.get("form_id")
        user_id = data.get("user_id")
        query = f"SELECT first_qid,spreadsheetId FROM form WHERE form_id = {form_id} AND user_id = {user_id}"
        result = db.execute_query(query)
        if len(result[0]) != 2:
            return {"data": "No such form exists"}
        

        first_qid=result[0][0]
        spreadsheet_id=result[0][1]
        prev_qid = data.get("prev_qid")
        next_qid = None
        if prev_qid == 0:
            next_qid = first_qid
            query = f"INSERT INTO question(form_id,ques_text,ques_type,next_qid) VALUES {form_id,data.get('ques_text'),data.get('ques_type'),next_qid}"
            qid = db.execute_query(query, True)
            query = f"UPDATE form SET first_qid={qid} WHERE form_id={form_id}"
            db.execute_query(query)
        else:
            query = f"SELECT next_qid FROM question WHERE q_id={prev_qid}"
            next_qid = db.execute_query(query)[0][0]
            query = f"INSERT INTO question(form_id,ques_text,ques_type,next_qid,prev_qid) VALUES {form_id,data.get('ques_text'),data.get('ques_type'),next_qid,prev_qid}"
            qid = db.execute_query(query, True)
            query = f"UPDATE question SET next_qid={qid} WHERE q_id={prev_qid}"
            db.execute_query(query)
        if(data.get('ques_type').upper()=='MCQ'):
            for resp in data.get('responses'):
                query = f"INSERT INTO response(q_id,res_text) VALUES {qid,resp}"
                db.execute_query(query,True)
        db.commit_transaction()


        insert_ques(spreadsheet_id,prev_qid,qid,data.get('ques_text'))
        
        return jsonify({"data":qid})

    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message})


@ques_bp.route("/update", methods=["POST"])
def update_ques():
    try:
        data = request.get_json()

        if "user_id" not in data.keys():
            return jsonify({"data": "user_id/username not added"})
        if "form_id" not in data.keys():
            return jsonify({"data": "form_id not added"})

        db = DatabaseTransaction()
        db.start_transaction()

        form_id = data.get("form_id")
        user_id = data.get("user_id")
        query = f"SELECT first_qid FROM form WHERE form_id = {form_id} AND user_id = {user_id}"
        result = db.execute_query(query)
        if len(result[0]) != 1:
            return {"data": "No such form exists"}

        form_id = data.get("form_id")
        q_id = data.get("q_id")
        query = f"SELECT spreadsheetId FROM form WHERE form_id = {form_id}"
        result = db.execute_query(query)
        if len(result[0]) != 1:
            return {"data": "No such question exists"}
        spreadsheet_id = result[0][0]
        query = f"UPDATE question SET ques_text='{data.get("ques_text")}' WHERE q_id={data.get("q_id")}"
        db.execute_query(query)
        db.commit_transaction()

        upd_ques(spreadsheet_id,q_id,data.get("ques_text"))
        return jsonify({"data":"Question Updated"})

    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message})


@ques_bp.route("/delete", methods=["DELETE"])
def delete_ques():
    try:
        data = request.get_json()

        if "user_id" not in data.keys():
            return jsonify({"data": "user_id/username not added"})
        if "form_id" not in data.keys():
            return jsonify({"data": "form_id not added"})

        db = DatabaseTransaction()
        db.start_transaction()
        form_id = data.get("form_id")
        user_id = data.get("user_id")
        query = f"SELECT spreadsheetId FROM form WHERE form_id = {form_id} AND user_id = {user_id}"
        result = db.execute_query(query)
        if (len(result) != 1) or (len(result[0]) != 1):
            return {"data": "No such form exists"}
        spreadsheet_id=result[0][0]


        form_id = data.get("form_id")
        q_id = data.get("q_id")
        query = f"SELECT prev_qid FROM question WHERE form_id = {form_id} AND q_id = {q_id}"
        result = db.execute_query(query)
        if len(result[0]) != 1:
            return {"data": "No such question exists"}
        prev_qid = result[0][0]


        query = f"SELECT next_qid FROM question WHERE q_id = {q_id}"
        next_qid = db.execute_query(query)[0][0]


        if prev_qid == None:
            query = f"UPDATE form SET first_qid={next_qid} WHERE form_id={form_id}"
            db.execute_query(query)
        else:
            query = f"UPDATE question SET next_qid={next_qid} WHERE q_id={prev_qid}"
            db.execute_query(query)

        query = f"DELETE FROM answer_text WHERE q_id={q_id}"
        db.execute_query(query)
        query = f"DELETE FROM answer_mcq WHERE q_id={q_id}"
        db.execute_query(query)
        query = f"DELETE FROM question WHERE q_id={q_id}"
        db.execute_query(query)
        db.commit_transaction()


        del_ques(spreadsheet_id,q_id)
        return jsonify({"data":"question deleted successfully"})

    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return jsonify({"data": error_message})
