from models import todos
import sql_function



class TodosDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
    
    def create_connection(self):
        return todos.create_connection(self.db_file)

    def initial(self):
        with self.create_connection() as conn:
            todos.execute_sql(conn, sql_function.create_projects_sql)
            todos.execute_sql(conn, sql_function.create_tasks_sql)

    def list(self):
        with self.create_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM projects")
            rows_p = cur.fetchall()
            cur.execute(f"SELECT * FROM tasks")
            rows_t = cur.fetchall()
        return rows_p, rows_t

    def add_project(self, name, start_date, end_date):
        with self.create_connection() as conn:
            todos.add_projekt(conn, name, start_date, end_date)
            conn.commit()
 
    def add_task(self, project_id, name, description, status, start_date, end_date):
        with self.create_connection() as conn:
            rows_p_no=len(todos.select_all(conn, "projects"))    
            if project_id<=rows_p_no:    
                todos.add_task(conn, project_id, name, description, status, start_date, end_date)
                conn.commit()

    def update(self, table, table_id, column, value):
        with self.create_connection() as conn:
            todos.update(conn, table, table_id, column, value)

    def delete(self, table, table_id):
        with self.create_connection() as conn:
            todos.delete_where(conn, table, table_id)
            conn.commit()



todos_database = TodosDatabase("database.db")
