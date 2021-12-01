from flask import Flask
from db_helpers import todos_database


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/api/v1/todos/init", methods=["GET"])
def init():
    return todos_database.initial()

@app.route("/api/v1/todos/", methods=["GET"])
def get_all():
    return todos_database.list()

@app.route("/api/v1/todos/add_p", methods=["POST"])
def add_project():
    name="Kodilla"
    start_date= "2021-05-11 00:00:00"
    end_date= "2021-05-13 20:00:00"
    return todos_database.add_project(name, start_date, end_date)

@app.route("/api/v1/todos/add_t/<int:project_id>", methods=["POST"])
def add_task(project_id): 
    name= "Czasowniki regularne"
    description="Zapamiętaj czasowniki ze strony 30"
    status="started"
    start_date="2022-05-11 12:00:00"
    end_date="2022-05-11 15:00:00"
    return todos_database.add_task(project_id, name, description, status, start_date, end_date)

@app.route("/api/v1/todos/<int:table_id>", methods=["PUT"])
def update(table_id):
    table="tasks"
    column="status"
    value="ended"
    return todos_database.update(table, table_id, column, value)


@app.route("/api/v1/todos/<int:table_id>", methods=['DELETE'])
def delete(table_id):
    table="tasks"
    return todos_database.delete(table, table_id)

if __name__ == "__main__":
    app.run(debug=True)