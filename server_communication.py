import requests
import json


def login(
        url="http://localhost:8080",
        myjson=None
):
    response = requests.post(url + "/user/login", json=myjson)
    data = json.loads(response.text)

    print(data)

    return data['token']


def join_game(
        url="http://localhost:8080",
        token="tokenn",
):
    response = requests.get(url + "/game/joinGame", headers={'Authorization': 'Bearer ' + token})
    data = json.loads(response.text)

    return data['playerIdx'], data['gameState']

def game_make_move(token, action, )