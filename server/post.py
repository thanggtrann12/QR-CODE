import json
from sre_constants import FAILURE, SUCCESS
import requests


headers = {"Content-Type": "application/json; charset=utf-8"}
url = "http://qthcmute.ddns.net:81/vehicle/getIn"


def post(user_info, car_info):
    data = json.loads(car_info)
    try:
        body = {
            "username": user_info,
            "type": "IN",
            "id": {
                "vehicleColor": data['vehicleColor'],
                "block": "string",
                "slotId": "string",
                "twoFirstDigits": data['twoFirstDigits'],
                "fourLastDigits": data['fourLastDigits'],
                "licensePlates": data['licensePlates'],
            }
        }
        print(str(body).replace("'", '"'))
        response = requests.post(url, json = json.loads(str(body).replace("'", '"')), headers=headers)
        if response.status_code == 200:
            return SUCCESS
        else:
            return FAILURE, response.status_code
    except Exception as e:
        print(e)
        return FAILURE, e
