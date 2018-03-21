import argparse
import os
import tempfile
import json

parser = argparse.ArgumentParser()
parser.add_argument("--key", help='input key')
parser.add_argument("--value", help="values")
args = parser.parse_args()
args.key = 'asd'
args.value = 'a123'
storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
f = open(storage_path, 'r')
string_json = f.read()
f.close()
if args.key and args.value:
    with open(storage_path, 'w+') as f:
        if string_json:
            key_value_storage = json.loads(string_json)
        else:
            key_value_storage = {}

        if args.key in key_value_storage:
            key_value_storage[args.key].extend(args.value.split(" "))
        else:
            key_value_storage[args.key] = args.value.split(" ")
        f.write(json.dumps(key_value_storage))
elif args.key and args.value is None:
    if args.key in json.loads(string_json):
        print(", ".join(json.loads(string_json)[args.key]))
    else:
        print('нет такого')
else:
    print('Не ввидены параметры')
