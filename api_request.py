import requests
import json

url = 'http://localhost:5000/api/'
hdr = {'Content-Type': 'application/json'}


def send(operation: str, par1: str, par2 = "") -> dict:
    def compose_data(operation: str, par1: str, par2 = "") -> dict:
        match operation:
            case 'login' | 'logout':
                return {"miner_ip": par1}
            case 'curtail':
                return {"token": par1, "mode": par2}
            case 'profileset':
                return{"token": par1, "profile": par2}
            case _:
                return {}

    req_url = url + operation
    req_data = compose_data(operation, par1, par2)

    if not req_data:
        print('you must be giving wrong operation!!!')
        exit(1)

    try:
        response = requests.post(req_url, headers=hdr, data=json.dumps(req_data))
    except requests.exceptions.RequestException as e:
        print("error in request: ", e)

    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        print("\t" + json.loads(response.content)['message'])
        return {}