from flask import Flask
from flask import request
from flask import jsonify
import json

app = Flask(__name__)
languages = []


@app.route('/languages', methods=['POST'])
def create_languages():
    body = json.load(request.data)
    languages.append(body)
    return jsonify(body)


@app.route("/languages/<language>", methods=['GET'])
def get_language_by_key(language):
    result = [item for item in languages if item["language"] == language]
    if len(result) > 0:
        return jsonify(result[0])
    else:
        return jsonify({"status": "not found"})


@app.route("/languages/<language>", methods=['DELETE'])
def delele_language(language):
    global languages
    languages = [item for item in languages if item["language"] != language]
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run()