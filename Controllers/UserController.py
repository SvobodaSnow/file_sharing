import sqlite3

from Signatures.Division import Division
from Signatures.Position import Position
from Signatures.User import User

connection = sqlite3.connect('my_database.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
email TEXT NOT NULL UNIQUE,
id_division INTEGER NOT NULL,
id_position INTEGER NOT NULL,
date_employment INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Division (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Position (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL UNIQUE
)
''')

connection.commit()


def add_user(user):
    cursor.execute('INSERT INTO Users (name, email, id_division, id_position, date_employment) VALUES (?, ?, ?, ?, ?)',
                   (user.name, user.email, user.division, user.position, user.date_employment)
                   )
    connection.commit()
    return


def update_user(user):
    cursor.execute('UPDATE Users SET name = ?, email = ?, id_division = ?, id_position = ?, date_employment = ? '
                   'WHERE id = ?', (user.name, user.email, user.division, user.position,
                                    user.date_employment, user.id))
    connection.commit()
    return


def delete_user_by_id(id):
    cursor.execute('DELETE Users WHERE id = ?', (id,))
    connection.commit()
    return


def add_division(division):
    cursor.execute('INSERT INTO Division (title) VALUES (?)', (division.title,))
    connection.commit()
    return


def add_position(position):
    cursor.execute('INSERT INTO Position (title) VALUES (?)', (position.title,))
    connection.commit()
    return


def get_division_by_id(id_division):
    cursor.execute('SELECT * FROM Division WHERE id = ?', (id_division,))
    d = cursor.fetchone()
    return division_from_sql(d) if d is not None else None


def get_position_by_id(id_position):
    cursor.execute('SELECT * FROM Position WHERE id = ?', (id_position,))
    p = cursor.fetchone()
    return position_from_sql(p) if p is not None else None


def get_all_divisions():
    cursor.execute('SELECT * FROM Division')
    return divisions_from_sql()


def get_all_position():
    cursor.execute('SELECT * FROM Position')
    return positions_from_sql()


def get_all_users():
    cursor.execute('SELECT * FROM Users')
    return users_from_sql()


def get_user_by_id(id):
    cursor.execute('SELECT * FROM Users WHERE id = ?', (id,))
    u = cursor.fetchone()
    return user_from_sql(u) if u is not None else None


def get_users_by_id(list_id):
    cursor.execute(f'SELECT * FROM Users WHERE id IN ({list_id})')
    return users_from_sql()


def get_users_by_name(name):
    cursor.execute(f"SELECT * FROM Users WHERE name LIKE '%{name}%'")
    return users_from_sql()


def get_users_by_email(email):
    cursor.execute(f"SELECT * FROM Users WHERE email LIKE '%{email}%'")
    return users_from_sql()


def get_users_by_division(id_division):
    cursor.execute("SELECT * FROM Users WHERE id_division = ?", id_division)
    return users_from_sql()


def get_users_by_position(id_position):
    cursor.execute("SELECT * FROM Users WHERE id_position = ?", id_position)
    return users_from_sql()


def get_users_by_date_employment(date_employment):
    cursor.execute(f"SELECT * FROM Users WHERE date_employment LIKE '%{date_employment}%'")
    return users_from_sql()


def users_from_sql():
    users = []
    for u in cursor.fetchall():
        users.append(user_from_sql(u))
    return users


def user_from_sql(sql):
    return User(sql[1], sql[2], get_division_by_id(sql[3]), get_position_by_id(sql[4]), sql[5], sql[0])


def divisions_from_sql():
    divisions = []
    for d in cursor.fetchall():
        divisions.append(division_from_sql(d))
    return divisions


def division_from_sql(sql):
    return Division(sql[1], sql[0])


def positions_from_sql():
    position = []
    for p in cursor.fetchall():
        position.append(position_from_sql(p))
    return position


def position_from_sql(sql):
    return Position(sql[1], sql[0])
