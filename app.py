from flask import Flask
from models import todos
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
    conn.close()
    return f"Projects:\n{rows_p}\nTasks:\n{rows_t}"


@app.route("/api/v1/todos/add_p", methods=["POST"])
def todos_add_p():
    db_file = "database.db"
    conn = todos.create_connection(db_file)
    rows_p_no=todos.add_projekt(conn, sql_data.projekt, sql_function.sql_projects)
    conn.commit()
    print_projects=todos.select_all(conn, "projects")
    conn.close()
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
        conn.close()
        return f"{print_tasks}"
    else:
        conn.close()
        return "Nie ma takiego projektu"

@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    db_file = "database.db"
    conn = todos.create_connection(db_file)
    todos.update(conn, "tasks", todo_id, status="ended")
    conn.close()
    return f"Zaktualizowano task: {todo_id}"


@app.route("/api/v1/todos/<int:todo_id>", methods=['DELETE'])
def delete_todo(todo_id):

    db_file = "database.db"
    conn = todos.create_connection(db_file)
    todos.delete_where(conn, "tasks", todo_id)
    conn.commit()
    conn.close()
    return f"Usunięto task: {todo_id}"


if __name__ == "__main__":
    app.run(debug=True)