import sqlite3
from sqlite3 import Error


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

    def add_projekt(self, conn, projekt, sql):
        cur = conn.cursor()
        cur.execute(sql, projekt)
        conn.commit()
        return cur.lastrowid

    def add_zadanie(self, conn, zadanie, sql):
        cur = conn.cursor()
        cur.execute(sql, zadanie)
        conn.commit()
        return cur.lastrowid

    def select_all(self, conn, table):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        return rows

    def update(self, conn, table, id, **kwargs):
        parameters = [f"{k} = ?" for k in kwargs]
        parameters = ", ".join(parameters)
        values = tuple(v for v in kwargs.values())
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
