import json

python_language = {
   "language": "python",
   "author": "Rossum"
}

json_string = json.dumps(python_language)
print(type(json_string))
print(json_string)
