from flask import Flask, jsonify
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'HELLO BEGIN FLASK!'


# add a new api
course = [
        {'name': 'Nguyen Van A',
        'id': '1',
        'class': '10B2'},
        {'name': 'Nguyen Van B',
        'id': '2',
        'class': '10B3'},
        {'name': 'Nguyen Van C',
        'id': '3',
        'class': '10B5'}
        ]


@app.route('/duyngudao', methods=['GET'])
def get_names():
    return jsonify({'List': course})


@app.route('/duyngudao/<int:list_id>', methods=['GET'])
def get_id(list_id):
    return jsonify({'list': course[list_id]})


# curl -i -H 'Content-Type: Application/json' -X POST http://localhost:5000/duyngudao
@app.route('/duyngudao', methods=['POST'])
def create():
    data = {'name': 'Nguyen Van D',
            'id': '4',
            'class': '10B2'}
    course.append(data)
    return jsonify({'Created': course})


# curl -i -H 'Content-Type: Application/json' -X PUT http://localhost:5000/duyngudao/2
@app.route('/duyngudao/<int:list_id>', methods=['PUT'])
def update_id(list_id):
    course[list_id]['class'] = '10B6'
    return jsonify({'List': course[list_id]})


# curl -i -H 'Content-Type: Application/json' -X DELETE http://localhost:5000/duyngudao/1
@app.route('/duyngudao/<int:list_id>', methods=['DELETE'])
def delete_id(list_id):
    course.remove(course[list_id])
    return jsonify({'Result': True})


if __name__ == '__main__':
    app.run()
