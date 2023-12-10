import requests
import json


def login(base_url, myjson):
    response = requests.post(base_url + "/user/login", json=myjson)
    data = json.loads(response.text)

    print(data)

    return data['token']


def join_game(base_url, token):
    response = requests.get(base_url + "/game/joinGame", headers={'Authorization': 'Bearer ' + token})
    data = json.loads(response.text)

    return data['playerIdx'], data['gameState']


def game_make_move(base_url, token, action, q, r, timeout=15):
    action_str = f"{action},{q},{r}"
    action_json = {'action': action_str}
    response = requests.post(base_url + "/game/doAction", headers={'Authorization': 'Bearer ' + token},
                             json=action_json, timeout=timeout)

    data = json.loads(response.text)

    return data['gameState']


def game_train(base_url, token, mapName, playerIdx):
    train_json = {'mapName': mapName, 'playerIdx': playerIdx}

    response = requests.post(base_url + "/game/train", headers={'Authorization': 'Bearer ' + token}, json=train_json)

    print(response.text)

    return response.text


def game_make_move_train(base_url, token, action, q, r):
    action_str = f"{action},{q},{r}"
    action_json = {'action': action_str}

    response = requests.post(base_url + "/game/actionTrain", headers={'Authorization': 'Bearer ' + token},
                             json=action_json)

    print(response.text)

    retu