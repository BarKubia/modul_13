from models import todos
import sql_function
import sql_data


def todos_list_api_v1_init():
    db_file = "database.db"
    conn = todos.create_connection(db_file)
    if conn is not None:
        todos.execute_sql(conn, sql_function.create_projects_sql)
        todos.execute_sql(conn, sql_function.create_tasks_sql)
        conn.close()
        return "Utworzono bazę danych" 

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

def todos_add_p():
    db_file = "database.db"
    conn = todos.create_connection(db_file)
    rows_p_no=todos.add_projekt(conn, sql_data.projekt, sql_function.sql_projects)
    conn.commit()
    print_projects=todos.select_all(conn, "projects")
    conn.close()
    return f"{print_projects}\n{rows_p_no}"

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

def update_todo(todo_id):
    db_file = "database.db"
    conn = todos.create_connection(db_file)
    todos.update(conn, "tasks", todo_id, status="ended")
    conn.close()
    return f"Zaktualizowano task: {todo_id}"

def delete_todo(todo_id):

    db_file = "database.db"
    conn = todos.create_connection(db_file)
    todos.delete_where(conn, "tasks", todo_id)
    conn.commit()
    conn.close()
    return f"Usunięto task: {todo_id}"
