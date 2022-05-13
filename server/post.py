from turtle import color
import requests


headers = {"Content-Type": "application/json; charset=utf-8"}
url = "http://qthcmute.ddns.net:81/vehicle/getIn"


def full_data_post_request(data):
    body = {
        "username": data['username'],
        "type": "IN",
        "id": 
            {
            "twoFirstDigits": str(data['twoFirstDigits']),
            "vehicleColor": str(data['vehicleColor']),
            "block": str(data['block']),
            "slotId": str(data['slotId']),
            "fourLastDigits": str(data['fourLastDigits'])
            }
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return True
    else:
        return False
