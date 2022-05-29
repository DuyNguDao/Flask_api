from flask import request
from flask import Flask
import json


app = Flask(__name__)


# lay thong tin query param trong request gui len, vd: localhost:5000/languages?name=python&order=desc
@app.route('/duyngudao')
def get_names():
    print(request.args)
    print(request.args.get('name'))
    return 'DAO DUY NGU'


if __name__ == '__main__':
    app.run()