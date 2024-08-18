import sqlite3

from Controllers import UserController
from Signatures.Project import Project
from Signatures.Status import Status
from Signatures.Task import Task

connection = sqlite3.connect('my_database.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Task (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT NOT NULL,
status TEXT NOT NULL,
id_project INTEGER NOT NULL,
id_owner INTEGER NOT NULL,
id_executors TEXT NOT NULL,
id_reviewers TEXT NOT NULL,
id_observers TEXT NOT NULL,
time_create INTEGER NOT NULL,
time_change INTEGER NOT NULL,
time_fulfilment INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Statuses (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Projects (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL UNIQUE
)
''')

connection.commit()


def add_task(task):
    cursor.execute(
        'INSERT INTO Task '
        '(title, description, status, id_project, id_owner, id_executors, id_reviewers,'
        'id_observers, time_create, time_change, time_fulfilment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (task.title, task.description, task.status, task.project, task.owner, list_to_string(task.executor),
         list_to_string(task.reviewers), list_to_string(task.observers), task.time_create, task.time_change,
         task.time_fulfilment)
    )
    connection.commit()
    return get_id_last_task()


def add_status(status):
    cursor.execute('INSERT INTO Statuses (title) VALUES (?)', (status.title,))
    connection.commit()
    return


def add_project(project):
    cursor.execute('INSERT INTO Projects (title) VALUES (?)', (project.title,))
    connection.commit()
    return


def get_status_by_id(id_status):
    cursor.execute('SELECT * FROM Statuses WHERE id = ?', (id_status,))
    d = cursor.fetchone()
    return status_from_sql(d) if d is not None else None


def get_project_by_id(id_project):
    cursor.execute('SELECT * FROM Projects WHERE id = ?', (id_project,))
    p = cursor.fetchone()
    return project_from_sql(p) if p is not None else None


def projects_from_sql():
    projects = []
    for d in cursor.fetchall():
        projects.append(project_from_sql(d))
    return projects


def project_from_sql(sql):
    return Project(sql[1], sql[0])


def statuses_from_sql():
    statuses = []
    for p in cursor.fetchall():
        statuses.append(status_from_sql(p))
    return statuses


def status_from_sql(sql):
    return Status(sql[1], sql[0])


def get_task_by_id(id):
    cursor.execute('SELECT * FROM Task WHERE id = ?', (id,))
    task = cursor.fetchone()
    return task_from_sql(task) if task is not None else None


def get_all_tasks():
    cursor.execute('SELECT * FROM Task')
    return tasks_from_sql()


def tasks_from_sql():
    tasks = []
    for t in cursor.fetchall():
        tasks.append(task_from_sql(t))
    return tasks


def task_from_sql(sql):
    return Task(
        id=sql[0],
        title=sql[1],
        description=sql[2],
        status=sql[3],
        project=sql[4],
        owner=UserController.get_user_by_id(sql[5]),
        executor=UserController.get_users_by_id(sql[6]),
        reviewers=UserController.get_users_by_id(sql[7]),
        observers=UserController.get_users_by_id(sql[8]),
        time_create=sql[9],
        time_change=sql[10],
        time_fulfilment=sql[11]
    )


def get_id_last_task():
    cursor.execute('SELECT id FROM Task ORDER BY id DESC LIMIT 1')
    return cursor.fetchone()[0]


def list_to_string(li):
    s = ''
    for ls in li:
        s += str(ls) + ', '
    return s[:-2]
