import json

json_string = '{"language": "python", "author": "Rossum"}'

python_language = json.loads(json_string)

print(type(python_language))

print(python_language)