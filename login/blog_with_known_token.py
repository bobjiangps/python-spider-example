import requests
import json


if __name__ == "__main__":
    url = "http://127.0.0.1:8000/automation/api/login/"
    user_info = {"username": "Basic",
                 "password": "test1234"}
    response = requests.post(url, data=user_info)
    print(response.status_code)
    server_user_data = json.loads(response.text)
    print(server_user_data)
    print(server_user_data["token"])