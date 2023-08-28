import json


def is_valid_json(data):
    if False == isinstance(data, str):
        # print(data)
        return False
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False
    
if __name__ == "__main__":
    is_valid_json({'as3':1,'as1':2})