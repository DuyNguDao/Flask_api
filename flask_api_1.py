from flask import Flask, request, jsonify, abort, url_for
from flask import make_response
from flask_httpauth import HTTPBasicAuth

# initialize flask
app = Flask(__name__)
# initialize secure
auth = HTTPBasicAuth()
# ********************PROGRAM INTERFACE API FLASK FOR CLIENT-SERVER***********************

# database

tasks = [{'id': 1,
         'title': 'Flask api for beginner',
          'description': 'POST, GET, PUT, PATCH, DELETE',
          'done': False},
         {'id': 2,
          'title': 'Python for beginner',
          'description': 'LIST, DICT, ARRAY',
          'done': False},
         {'id': 3,
          'title': 'AI for beginner',
          'description': 'MC, DEEP',
          'done': False}]


# *****************  BUILD FIVE SERVICE WEB FOR CLIENT ***********************
# ----------------------------------------------------------------------
# build method GET
# check: $ curl -i -X GET http://localhost:5000/duyngudao/api/v.1/data_task
# note: if have login_required then use:
# curl -u flask:python -i -X GET  http://localhost:5000/duyngudao/api/v.1/data_task
@app.route('/duyngudao/api/v.1/data_task', methods=['GET'])
@auth.login_required
def get_data():
    return jsonify({'task': tasks})


# -----------------------------------------------------------------------
# build method GET with id
# check: $ curl -i -X GET http://localhost:5000/duyngudao/api/v.1/data_task/0
@app.route('/duyngudao/api/v.1/data_task/<int:task_id>', methods=['GET'])
@auth.login_required
def get_id(task_id):
    # get folder data have id from request
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404, 'Not Found')  # respond error 404 html
    # respond data
    return jsonify({'task': task[0]})


# -----------------------------------------------------------------------
# Respond error 404 json
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


# -----------------------------------------------------------------------
# append folder -> data
# build method POST
# check: curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Build api with flask python",
# "description": "Understand about methods GET, POST,..."}' http://localhost:5000/duyngudao/api/v.1/data_task
@app.route('/duyngudao/api/v.1/data_task', methods=['POST'])
def creak_task():
    # check file json and file information
    if not request.json or not 'title' in request.json:
        abort(400)
    # create new task folder have data
    task = {'id': tasks[-1]['id'] + 1,
            'title': request.json['title'],
            'description': request.json.get('description', ''),
            'done': False}
    # append new task
    tasks.append(task)
    # respond
    return jsonify({'task': task}), 201


# -----------------------------------------------------------------------------
# build method PUT
# method PUT append data new-> data (PUT < POST)
# check: curl -i -H "Content-Type: application/json" -X PUT -d '{"title":"python expand", "description":"class, set,
# ...", "done":true}' http://localhost:5000/duyngudao/api/v.1/data_task/2
@app.route('/duyngudao/api/v.1/data_task/<int:task_id>', methods=['PUT'])
def put_data(task_id):
    # find task_id in data
    task = [task for task in tasks if task['id'] == task_id]
    # check id
    if len(task) == 0:
        abort(404, 'Not Found')
    # check json from request
    if not request.json:
        abort(400)
    # check format title, description, done if have title, ...
    if 'title' in request.json and type(request.json['title']) is not str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    # update data is data 1 if not None
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    # respond
    return jsonify({'task': task[0]})


# -------------------------------------------------------------------------------------------
# build methods DELETE
# delete task in data
# check: $ curl -i -X DELETE http://localhost:5000/duyngudao/api/v.1/data_task/0
@app.route('/duyngudao/api/v.1/data_task/<int:task_id>', methods=['DELETE'])
def delete_data(task_id):
    # check task id
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404, 'Not Found')
    tasks.remove(task[0])
    return jsonify({'result': True})


# -----------------------------------------------------------------------------------
# improve service
# return url id use url_for
# build function
def make_public_task_id(task):
    # create new json
    new_task = {}
    # check field in task and create url and change for field id
    for field in task:
        if field == 'id':
            # change 'id' = 'uri' and number_id = url
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


# build service GET
@app.route('/duyngudao/api/v.1/data_task', methods=['GET'])
def get_task():
    return jsonify({'tasks': [make_public_task_id(task) for task in tasks]})


# ---------------------------------------------------------------------------------
# securing service web
# build user and password
@auth.get_password
def get_password(username):
    if username == 'flask':
        # password = python
        return 'python'
    return None


# build error
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


if __name__ == '__main__':
    app.run(debug=True)
