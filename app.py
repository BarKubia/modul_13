from flask import Flask, jsonify
from models import todos
from flask import abort
from flask import make_response
from flask import request

import sqlite3
from sqlite3 import Error
import sql_function
import sql_data


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/api/v1/todos/init", methods=["GET"])
def todos_list_api_v1_init():
    db_file = "database.db"
    conn = todos.create_connection(db_file)
    if conn is not None:
        todos.execute_sql(conn, sql_function.create_projects_sql)
        todos.execute_sql(conn, sql_function.create_tasks_sql)
        conn.close()
        return "Utworzono bazę danych" 


@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():
    db_file = "database.db"
    conn = todos.create_connection(db_file)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM projects")
    rows_p = cur.fetchall()
    cur.execute(f"SELECT * FROM tasks")
    rows_t = cur.fetchall()
    return f"Projects:\n{rows_p}\nTasks:\n{rows_t}"


@app.route("/api/v1/todos/add_p", methods=["POST"])
def todos_add_p():
    db_file = "database.db"
    conn = todos.create_connection(db_file)
    rows_p_no=todos.add_projekt(conn, sql_data.projekt, sql_function.sql_projects)
    conn.commit()
    print_projects=todos.select_all(conn, "projects")
    return f"{print_projects}\n{rows_p_no}"



@app.route("/api/v1/todos/add_t/<int:pr_id>", methods=["POST"])
def todos_add_t(pr_id):
    db_file = "database.db"
    conn = todos.create_connection(db_file)
    print_projects=todos.select_all(conn, "projects")
    rows_p_no=len(print_projects)
    if pr_id<=rows_p_no:
        todos.add_zadanie(conn, sql_data.funct_zadanie(pr_id), sql_function.sql_tasks)
        conn.commit()
        print_tasks=todos.select_all(conn, "tasks")
        return f"{print_tasks}"
    else:
        return "Nie ma takiego projektu"


# def create_todo():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     todo = {
#         'id': todos.all()[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     todos.create(todo)
#     return jsonify({'todo': todo}), 201

# @app.route("/api/v1/todos/<int:todo_id>", methods=["GET"])
# def get_todo(todo_id):
#     todo = todos.get(todo_id)
#     if not todo:
#         abort(404)
#     return jsonify({"todo": todo})


# @app.route("/api/v1/todos/<int:todo_id>", methods=['DELETE'])
# def delete_todo(todo_id):
#     result = todos.delete(todo_id)
#     if not result:
#         abort(404)
#     return jsonify({'result': result})

# @app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
# def update_todo(todo_id):
#     todo = todos.get(todo_id)
#     if not todo:
#         abort(404)
#     if not request.json:
#         abort(400)
#     data = request.json
#     if any([
#         'title' in data and not isinstance(data.get('title'), str),
#         'description' in data and not isinstance(data.get('description'), str),
#         'done' in data and not isinstance(data.get('done'), bool)
#     ]):
#         abort(400)
#     todo = {
#         'title': data.get('title', todo['title']),
#         'description': data.get('description', todo['description']),
#         'done': data.get('done', todo['done'])
#     }
#     todos.update(todo_id, todo)
#     return jsonify({'todo': todo})

# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

# @app.errorhandler(400)
# def bad_request(error):
#     return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)