import datetime
import os
import sqlite3

import Controllers.UserController as UserController
import Controllers.TaskController as TaskController
from Controllers import FileController
from Signatures.Division import Division
from Signatures.File import FileInfo
from Signatures.Position import Position
from Signatures.Task import Task
from Signatures.User import User
from flask import Flask, make_response, request, jsonify


app = Flask("user")


# Работа с чатом
@app.route('/chat')
def hello_chat():
    return 'Hello, Chat!'


# Работа с запросами
@app.route('/tasks', methods=['POST'])
def add_tasks():
    try:
        t_json = request.json
        task = Task(
            t_json['title'],
            t_json['description'],
            t_json['status'],
            t_json['project'],
            t_json['owner'],
            t_json['executor'],
            t_json['reviewers'],
            t_json['observers'],
            datetime.datetime.today(),
            datetime.datetime.today(),
            datetime.datetime.strptime(t_json['time_fulfilment'], '%Y-%m-%d %H:%M')
        )
        task.id = TaskController.add_task(task)
        if not os.path.exists(f'files/{task.project}'):
            os.mkdir(f'files/{task.project}')
        if not os.path.exists(f'files/{task.project}/{task.id}'):
            os.mkdir(f'files/{task.project}/{task.id}')
        return jsonify({'id': task.id})
    except sqlite3.IntegrityError:
        return make_response(jsonify({'error': 'Переданы неверные параметры'}), 400)


@app.route('/tasks')
def get_all_tasks():
    tasks = []
    query = request.args
    if query:
        if len(query) == 1 and 'id' in query.keys():
            task = TaskController.get_task_by_id(query['id'])
            return task.to_json() if task is not None else make_response(jsonify(), 204)
    else:
        for t in TaskController.get_all_tasks():
            tasks.append(t.to_json())
        return tasks


# Работа с файлами
@app.route('/files/tasks', methods=['POST'])
def add_file():
    files = request.files
    query = request.args
    if (query
            and 'owner' in query.keys()
            and 'project_id' in query.keys()
            and 'task_id' in query.keys()
    ):
        project_id = query['project_id']
        task_id = query['task_id']
        owner = query['owner']
        for k in files.keys():
            name_file = files[k].filename
            path_file = f'files/{project_id}/{task_id}'
            if os.path.exists(path_file):
                files[k].save(path_file + f'/{name_file}')
                FileController.add_new_file_info(FileInfo(name_file, path_file, owner, task=task_id))
            else:
                return make_response(jsonify({'error': 'Переданы неверные параметры'}), 400)

        return jsonify({'state': 'successfully'})
    else:
        return make_response(jsonify({'error': 'Переданы неверные параметры'}), 400)


# Работа с пользователями
@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = User(
            request.json['name'],
            request.json['email'],
            request.json['idDivision'],
            request.json['idPosition'],
            request.json['date_employment']
        )
        if (UserController.get_division_by_id(user.division) is not None
                and UserController.get_position_by_id(user.position) is not None):
            UserController.add_user(user)
            return jsonify({'state': 'successfully'})
        else:
            return make_response(jsonify({'error': 'Переданы неверные параметры'}), 400)
    except sqlite3.IntegrityError:
        return make_response(jsonify({'error': 'Пользователь с данным email уже зарегистрирован'}), 400)


@app.route('/users', methods=['DELETE'])
def delete_user_by_id():
    query = request.args
    if query and 'id' in query.keys():
        UserController.delete_user_by_id(query['id'])
    else:
        return make_response(jsonify({'error': 'Переданы неверные параметры'}), 400)
    return jsonify({'state': 'successfully'})


@app.route('/users', methods=['PATCH'])
def update_user():
    try:
        js = request.json
        if 6 >= len(js) > 1 and 'id' in js:
            user = UserController.get_user_by_id(js['id'])
            if user:
                for j in js:
                    match j:
                        case 'name':
                            user.name = js['name']
                        case 'email':
                            user.email = js['email']
                        case 'date_employment':
                            user.date_employment = js['date_employment']
                        case 'idDivision':
                            user.division = js['idDivision']
                        case 'idPosition':
                            user.position = js['idPosition']

                UserController.update_user(user)
                return jsonify({'state': 'successfully'})
            else:
                return make_response(jsonify({'error': 'Пользователь для изменения не найден'}), 404)
        else:
            return make_response(jsonify({'error': 'Переданы неверные параметры'}), 400)
    except sqlite3.IntegrityError:
        return make_response(jsonify({'error': 'Пользователь с данным email уже зарегистрирован'}), 400)


@app.route('/users/divisions')
def get_all_divisions():
    divisions = []
    for d in UserController.get_all_divisions():
        divisions.append(d.to_json())
    return divisions


@app.route('/users/positions')
def get_all_positions():
    positions = []
    for p in UserController.get_all_position():
        positions.append(p.to_json())
    return positions


@app.route('/users/divisions', methods=['POST'])
def create_division():
    try:
        division = Division(
            request.json['title']
        )
        UserController.add_division(division)
        return jsonify({'state': 'successfully'})
    except sqlite3.IntegrityError:
        return make_response(jsonify({'error': 'Подразделение с данным названием уже зарегистрированно'}), 400)


@app.route('/users/positions', methods=['POST'])
def create_position():
    try:
        position = Position(
            request.json['title']
        )
        UserController.add_position(position)
        return jsonify({'state': 'successfully'})
    except sqlite3.IntegrityError:
        return make_response(jsonify({'error': 'Должность с данным названием уже зарегистрированна'}), 400)


@app.route('/users')
def get_users():
    users = []
    query = request.args
    if query:
        if len(query) == 1:
            if 'id' in query.keys():
                user = UserController.get_user_by_id(query['id'])
                return user.to_json() if user is not None else make_response(jsonify(), 204)
            elif 'name' in query.keys():
                for u in UserController.get_users_by_name(query['name']):
                    users.append(u.to_json())
                return users
            elif 'email' in query.keys():
                for u in UserController.get_users_by_email(query['email']):
                    users.append(u.to_json())
                return users
            elif 'id_division' in query.keys():
                for u in UserController.get_users_by_division(query['id_division']):
                    users.append(u.to_json())
                return users
            elif 'id_position' in query.keys():
                for u in UserController.get_users_by_position(query['id_position']):
                    users.append(u.to_json())
                return users
            elif 'date_employment' in query.keys():
                for u in UserController.get_users_by_date_employment(query['date_employment']):
                    users.append(u.to_json())
                return users
            else:
                make_response(jsonify({'error': 'Переданы неверные параметры'}), 400)
        else:
            return make_response(jsonify({'error': 'Передано более одного аргумента запроса'}), 400)
    else:
        for u in UserController.get_all_users():
            users.append(u.to_json())
        return users


def start_program():
    app.run(debug=True)
    return

