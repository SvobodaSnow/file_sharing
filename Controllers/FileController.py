import sqlite3

connection = sqlite3.connect('my_database.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Files_info (
id INTEGER PRIMARY KEY,
name_file TEXT NOT NULL UNIQUE,
path_file TEXT NOT NULL,
owner_id INTEGER NOT NULL,
task_id INTEGER
)
''')

connection.commit()


def add_new_file_info(file_info):
    cursor.execute(
        'INSERT INTO Files_info (name_file, path_file, owner_id, task_id) VALUES (?, ?, ?, ?, ?)',
        (file_info.name_file, file_info.path_file, file_info.owner, file_info.task)
    )
    connection.commit()
    return

