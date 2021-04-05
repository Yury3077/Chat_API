"""
REST API for chat
Module BANTON: waiting for request from client application
Do: create chat, delete chat, add new user to chat, remove user from chat
Use SQL DB -> select or insert

"""

from flask import Flask, request, make_response, jsonify
import pyodbc

app = Flask(__name__)


def import_azure():
    """
    Connection to microsoft AZURE database
    :return: connection with DB
    """
    server = 'letond.database.windows.net'
    database = 'mydatabase'
    username = ''
    password = ''
    driver = '{ODBC Driver 17 for SQL Server}'

    conn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return conn


@app.route('/api/banton/new_chat', methods=['POST'])
def create_chat():
    """
    add new chat from post request
    check dict from client and insert into BD
    :return: Response according to result
    if ok -> 200
    already exist -> 403
    incorrect data from client -> 400
    """
    if request.content_type != 'application/json':
        return make_response(jsonify({"response": "requests is not json format"}), 400)

    data = request.get_json()
    if len(data) != 2 or type(data) != dict:
        return make_response(jsonify({'answer': "Incorrect input data, ohhhhh"}), 400)
    if 'name_chat' not in data.keys() or 'descr' not in data.keys():
        return make_response(jsonify({'answer': "Incorrect input data, ohhhhh"}), 400)

    conn = import_azure()
    new_chat_name = data["name_chat"]
    desc_new_chat = data["descr"]
    with conn.cursor() as cursor:
        cursor.execute(f"select name_chat from chat_table where CONVERT(VARCHAR, name_chat) = '{new_chat_name}'")
        rows = cursor.fetchall()
        if len(rows) == 0:
            cursor.execute(f"INSERT INTO chat_table(name_chat, descr) VALUES('{new_chat_name}', '{desc_new_chat}')")
            return make_response(jsonify({'answer': "Chat have been created"}), 200)
        else:
            return make_response(jsonify({'answer': "This name already exist, try to use other"}), 403)


@app.route('/api/banton/remove_chat', methods=['POST'])
def del_chat():
    """
    delete a chat
    check dict from client and make changes into BD
    :return: Response according to result
    if ok -> 200
    not found -> 404
    incorrect data from client -> 400
    """
    if request.content_type != 'application/json':
        return make_response(jsonify({"response": "requests is not json format"}), 400)

    data = request.get_json()
    if len(data) != 1 or type(data) != dict:
        return make_response(jsonify({'answer': "Incorrect input data, ohhhhh"}), 400)
    if 'name_chat' not in data.keys():
        return make_response(jsonify({'answer': "Incorrect input data, ohhhhh"}), 400)

    conn = import_azure()
    del_chat_name = data["name_chat"]
    with conn.cursor() as cursor:
        cursor.execute(f"select name_chat from chat_table where CONVERT(VARCHAR, name_chat) = '{del_chat_name}'")
        rows = cursor.fetchall()
        if len(rows) >= 1:
            cursor.execute(f"DELETE FROM chat_table WHERE CONVERT(VARCHAR, name_chat) = '{del_chat_name}'")
            return make_response(jsonify({'answer': "The chat have been deleted"}), 200)
        else:
            return make_response(jsonify({'answer': "Not found name of chat"}), 404)


@app.route('/api/banton/new_user', methods=['POST'])
def new_user():
    """
    add new user to chat from post request
    check dict from client and insert  info into BD
    :return: Response according to result
    if ok -> 200
    incorrect data -> 400
    not found nick_name -> 403
    """
    if request.content_type != 'application/json':
        return make_response(jsonify({"response": "requests is not json format"}), 400)

    data = request.get_json()
    if len(data) != 2 or type(data) != dict:
        return make_response(jsonify({'answer': "Incorrect input data, ohhhhh"}), 400)
    if 'name_chat' not in data.keys() or 'nick_name' not in data.keys():
        return make_response(jsonify({'answer': "Incorrect input data, ohhhhh"}), 400)

    conn = import_azure()
    chat_name = data["name_chat"]
    nick_add = data["nick_name"]
    with conn.cursor() as cursor:
        cursor.execute(f"select ID from chat_table where CONVERT(VARCHAR, name_chat) = '{chat_name}'")
        rows1 = cursor.fetchall()
        cursor.execute(f"select ID from users where CONVERT(VARCHAR, nickname) = '{nick_add}'")
        rows2 = cursor.fetchall()

        if len(rows1) == 1 and len(rows2) == 1:
            int_row1 = rows1[0][0]
            int_row2 = rows2[0][0]
            cursor.execute(f"INSERT INTO many_to_many(name_chat_id, nickname_id) VALUES('{int_row1}', '{int_row2}')")
            return make_response(jsonify({'answer': "User have been added to the chat"}), 200)
        else:
            return make_response(jsonify({'answer': "No user with that nickname"}), 403)


@app.route('/api/banton/remove_user', methods=['POST'])
def del_user():
    """
    delete a user from the chat
    check dict from client application and make changes into BD
    :return: Response according to result
    ok -> 200
    incorrect data -> 400
    not found nick_name or name_chat -> 403
    """
    if request.content_type != 'application/json':
        return make_response(jsonify({"response": "requests is not json format"}), 400)

    data = request.get_json()
    if len(data) != 2 or type(data) != dict:
        return make_response(jsonify({'answer': "Incorrect input data, ohhhhh"}), 400)
    if 'name_chat' not in data.keys() or 'nick_name' not in data.keys():
        return make_response(jsonify({'answer': "Incorrect input data, ohhhhh"}), 400)

    conn = import_azure()
    chat_name = data["name_chat"]
    nick_del = data["nick_name"]
    with conn.cursor() as cursor:
        cursor.execute(f"select ID from chat_table where CONVERT(VARCHAR, name_chat) = '{chat_name}'")
        rows1 = cursor.fetchall()
        cursor.execute(f"select ID from users where CONVERT(VARCHAR, nickname) = '{nick_del}'")
        rows2 = cursor.fetchall()

        if len(rows1) == 1 and len(rows2) == 1:
            int_row1 = rows1[0][0]  # приведение к INT
            int_row2 = rows2[0][0]
            # Проверка существует ли такой пользователь в чате
            cursor.execute(f"SELECT * FROM many_to_many WHERE name_chat_id = {int_row1} AND nickname_id = {int_row2}")
            rows3 = cursor.fetchall()
            if len(rows3) >= 1:
                cursor.execute(f"DELETE from many_to_many WHERE name_chat_id = {int_row1} AND nickname_id = {int_row2}")
                return make_response(jsonify({'answer': "User have been deleted from the chat"}), 200)
            else:
                return make_response(jsonify({'answer': "Not found nick_name or name_chat"}), 403)


if __name__ == "__main__":
    app.run("127.0.0.1", port=8000)
