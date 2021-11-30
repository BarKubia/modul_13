create_projects_sql = """
-- projects table
CREATE TABLE IF NOT EXISTS projects (
    id integer PRIMARY KEY,
    nazwa text NOT NULL,
    start_date text,
    end_date text
);
"""
create_tasks_sql = """
-- zadanie table
CREATE TABLE IF NOT EXISTS tasks (
    id integer PRIMARY KEY,
    projekt_id integer NOT NULL,
    nazwa VARCHAR(250) NOT NULL,
    opis TEXT,
    status VARCHAR(15) NOT NULL,
    start_date text NOT NULL,
    end_date text NOT NULL,
    FOREIGN KEY (projekt_id) REFERENCES projects (id)
);
"""

sql_tasks = '''INSERT INTO tasks(projekt_id, nazwa, opis, status, start_date, end_date)
        VALUES(?,?,?,?,?,?)'''

sql_projects = '''INSERT INTO projects(nazwa, start_date, end_date)
                 VALUES(?,?,?)'''

