import sqlite3
from sqlite3 import Error
import sql_function


class Todos:
    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)                
            return conn
        except Error as e:
            print(e)
        return conn

    def execute_sql(self, conn, sql):
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

    def add_projekt(self, conn, name, start_date, end_date):
        projekt = (name, start_date, end_date)
        cur = conn.cursor()
        cur.execute(sql_function.sql_projects, projekt)
        conn.commit()

    def add_task(self, conn, project_id, name, description, status, start_date, end_date):
        
        task = (project_id, name, description, status, start_date, end_date)
        cur = conn.cursor()
        cur.execute(sql_function.sql_tasks, task)
        conn.commit()

    def select_all(self, conn, table):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        return rows

    def update(self, conn, table, id, parameter, value):
        parameters=parameter+" = ?"
        values = tuple([value])
        values += (id, )

        sql_update = f''' UPDATE {table}
                  SET {parameters}
                  WHERE id = ?'''
        try:
            cur = conn.cursor()
            cur.execute(sql_update, values)
            conn.commit()
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)

    def delete_where(self, conn, table, todo_id, **kwargs):
        qs = [f"id={todo_id}"]
        values = tuple()
        for k, v in kwargs.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)
        sql = f'DELETE FROM {table} WHERE {q}'
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("Deleted")


todos = Todos()
