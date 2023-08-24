import json


def is_valid_json(data):
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False