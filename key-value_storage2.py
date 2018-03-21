import argparse
import os
import tempfile
import json

def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()

parser = argparse.ArgumentParser()
parser.add_argument("--key", help='input key')
parser.add_argument("--value", help="values")
args = parser.parse_args()
#args.key = 'asd'
#args.value = 'asd, zxxzc'
storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
#if not os.path.exists(storage_path):
   # f=open(storage_path,'w')
   # f.close()
with open(storage_path, 'a+') as f:
    f.seek(0)
    json_string = f.read()
    deleteContent(f)

    if not json_string:
        key_value_storage = dict()

    else:

        key_value_storage = json.loads(json_string)
    if args.key and args.value:
        if args.key in key_value_storage:
            key_value_storage[args.key].extend(args.value.split(", "))
        else:
            key_value_storage[args.key] = []
            key_value_storage[args.key].extend(args.value.split(", "))
        f.write(json.dumps(key_value_storage))
    elif args.key and args.value is None:
        if args.key in key_value_storage:
            print(", ".join(key_value_storage[args.key]))
            f.write(json.dumps(key_value_storage))
        else:
            f.write(json.dumps(key_value_storage))
            print("")
    else:
        f.write(json.dumps(key_value_storage))
        print("")
