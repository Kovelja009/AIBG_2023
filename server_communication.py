import requests
import json

def login(base_url, myjson):
    response = requests.post(base_url + "/user/login", json=myjson)
    data = json.loads(response.text)

    # print(data)

    return data['token']


def join_game(base_url, token):
    response = requests.get(base_url + "/game/joinGame", headers={'Authorization': 'Bearer ' + token}, timeout=25)
    data = json.loads(response.text)

    return data['playerIdx'], data['gameState']


def game_make_move(base_url, token, action_json, timeout=15):
    response = requests.post(base_url + "/game/doAction", headers={'Authorization': 'Bearer ' + token},
                             json=action_json, timeout=timeout)

    data = json.loads(response.text)

    print(f'message: {data["message"]}')

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

    return response.text


def create_game(base_url, token):
    players_json = {
        "playerUsernames": ["debelizonger1", "debelizonger2", "debelizonger3", "debelizonger4"],
        "mapName": "test1.txt"
    }
    response = requests.post(base_url + "/game/createGame", headers={'Authorization': 'Bearer ' + token},
                             json=players_json, timeout=25)

    data = json.loads(response.text)
    print(data)
    return data