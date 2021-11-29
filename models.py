import json
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

    def select_zadanie_by_status(conn, status):
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE status=?", (status,))
        rows = cur.fetchall()
        return rows

    def select_all(self, conn, table):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        return rows

    def select_where(conn, table, **query):
        cur = conn.cursor()
        qs = []
        values = ()
        for k, v in query.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)
        cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
        rows = cur.fetchall()
        return rows


    # def get(self, id):



    #     todo = [todo for todo in self.all() if todo['id'] == id]
    #     if todo:
    #         return todo[0]
    #     return []

    # def create(self, data):
    #     self.todos.append(data)
    #     self.save_all()

    # def save_all(self):
    #     with open("todos.json", "w") as f:
    #         json.dump(self.todos, f)

    # def update(self, id, data):
    #     todo = self.get(id)
    #     if todo:
    #         index = self.todos.index(todo)
    #         self.todos[index] = data
    #         self.save_all()
    #         return True
    #     return False

    # def delete(self, id):
    #     todo = self.get(id)
    #     if todo:
    #         self.todos.remove(todo)
    #         self.save_all()
    #         return True
    #     return False


todos = Todos()
