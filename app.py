from flask import Flask
import db_helpers


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/api/v1/todos/init", methods=["GET"])
def init():
    return db_helpers.todos_list_api_v1_init()

@app.route("/api/v1/todos/", methods=["GET"])
def get_all():
    return db_helpers.todos_list_api_v1()

@app.route("/api/v1/todos/add_p", methods=["POST"])
def add_p():
    return db_helpers.todos_add_p()

@app.route("/api/v1/todos/add_t/<int:pr_id>", methods=["POST"])
def add_t(pr_id):
    return db_helpers.todos_add_t(pr_id)

@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update(todo_id):
    return db_helpers.update_todo(todo_id)

@app.route("/api/v1/todos/<int:todo_id>", methods=['DELETE'])
def delete(todo_id):
    return db_helpers.delete_todo(todo_id)

if __name__ == "__main__":
    app.run(debug=True)