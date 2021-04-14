import requests
import json
def createUserToApi(uuid, username):
    url = "http://localhost:9999/createuser"
    data = {
        "uid": uuid,
        "userName": username
    }
    headers = {
        "Content-Type": "application/json"
    }
    putter = requests.put(url, data=json.dumps(data), headers=headers)
    print(putter)


def file_transferto_api(uuid, username, filename,b64_encoded):
    url = "http://127.0.0.1:9999/upload"
    payload = json.dumps({
        "uid": uuid,
        "userName": username,
        "filename": filename,
        "b64_file": b64_encoded
    }, default=str)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    print(response.text)
