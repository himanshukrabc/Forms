from flask import Blueprint
from flask import request, jsonify
import pymysql
from assets.db import execute_query
from assets.sheets import create_sheet

form_bp = Blueprint("form", __name__)

@form_bp.route("/create", methods=["POST"])
def create_form():
    try:
        data = request.get_json()
        if "questions" not in data.keys():
            return jsonify({"data": "no questions added to form"})
        if "user_id" not in data.keys():
            return jsonify({"data": "user_id not added"})
        query = f"SELECT * FROM user WHERE user_id = '{data.get('user_id')}'"
        result = execute_query(query)
        if len(result) == 0:
            return jsonify({"data": "user not found"})

        first_qid = None
        query = f"INSERT INTO form(user_id) VALUES ({data.get('user_id')})"
        form_id = execute_query(query, True)

        prev_qid = None
        qid_list = []
        q_text_list = []
        for ques in data.get("questions"):
            if prev_qid == None:
                query = f"INSERT INTO question(form_id, ques_text, ques_type, prev_qid) VALUES ({form_id}, '{ques.get('ques_text')}', '{ques.get('ques_type')}', NULL)"
            else:
                query = f"INSERT INTO question(form_id,ques_text,ques_type,prev_qid) VALUES {form_id,ques.get('ques_text'),ques.get('ques_type'),prev_qid}"
            print(query)
            qid = execute_query(query, True)
            qid_list.append(qid)
            q_text_list.append(ques.get('ques_text'))
            prev_qid = qid
            if(first_qid==None):
                first_qid = qid
            if ques.get("ques_type") == "MCQ":
                for resp in ques.get("responses"):
                    query = f"INSERT INTO response(q_id,res_text) VALUES {qid,resp}"
                    execute_query(query, True)
        for i in range(len(qid_list)-1):
            query = f"UPDATE question SET next_qid={qid_list[i+1]} WHERE q_id={qid_list[i]}"
            execute_query(query)
        query = f"UPDATE form SET first_qid = {first_qid} WHERE form_id = {form_id}"
        execute_query(query)
        spreadsheetId = create_sheet(data.get('user_id'),qid_list,q_text_list)
        query = f"UPDATE form SET spreadsheetId = '{spreadsheetId}' WHERE form_id = {form_id}"
        execute_query(query)
        return jsonify({"form_id": form_id,"qid_list":qid_list,"spreadsheet_id":spreadsheetId})

    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return {"data": error_message}


@form_bp.route("/display", methods=["POST"])
def display_form():
    try:
        data = request.get_json()

        if "user_id" not in data.keys():
            return jsonify({"data": "user_id not added"})
        if "form_id" not in data.keys():
            return jsonify({"data": "form_id not added"})

        form_id = data.get("form_id")
        user_id = data.get("user_id")
        query = f"SELECT first_qid FROM form WHERE form_id = {form_id} AND user_id = {user_id}"
        result = execute_query(query)
        if len(result[0]) != 1:
            return {"data": "No such form exists"}

        query = f"SELECT * FROM question WHERE form_id = {form_id}"
        q_list = execute_query(query)

        mp = {}
        print(q_list)
        for q in q_list:
            mp[q[0]] = {"text": q[2], "type": q[3], "next_qid": q[4]}
        resp = []
        cur = result[0][0]
        while cur != None:
            if mp[cur].get("type").upper() == "MCQ":
                query = f"SELECT res_id,res_text FROM response WHERE q_id={cur}"
                result = execute_query(query)
                responses = []
                for item in result:
                    responses.append({"resp_id":item[0],"resp_text":item[1]})
                resp.append(
                {
                    "q_id": cur,
                    "q_text": mp[cur].get("text"),
                    "q_type": mp[cur].get("type"),
                    "response":responses
                })
            else:
                resp.append(
                {
                    "q_id": cur,
                    "q_text": mp[cur].get("text"),
                    "q_type": mp[cur].get("type"),
                })
            cur = mp[cur].get("next_qid")
        return jsonify({"data":resp})

    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return {"data": error_message}


@form_bp.route("/delete", methods=["DELETE"])
def delete_form():
    try:
        data = request.get_json()

        if "user_id" not in data.keys():
            return jsonify({"data": "user_id not added"})
        if "form_id" not in data.keys():
            return jsonify({"data": "form_id not added"})

        form_id = data.get("form_id")
        user_id = data.get("user_id")
        query = f"SELECT COUNT(*) FROM form WHERE form_id = {form_id} AND user_id = {user_id}"
        result = execute_query(query)
        if result[0][0] != 1:
            return {"data": "unexpected Error"}

        query = (
            f"SELECT q_id FROM question WHERE form_id = {form_id} AND ques_type = 'MCQ'"
        )
        qid_list = execute_query(query)[0]
        for qid in qid_list:
            query = f"DELETE FROM response WHERE q_id = {qid}"
            execute_query(query)
        query = f"DELETE FROM question WHERE form_id = {form_id}"
        execute_query(query)
        query = f"DELETE FROM form WHERE form_id = {form_id}"
        execute_query(query)
        return {"data": "Form deleted"}

    except pymysql.Error as e:
        print(e)
        error_message = f"Error executing query: {e}"
        return {"data": error_message}
