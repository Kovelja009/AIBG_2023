import json

import server_communication
import json_parser
from strategy_manager import StrategyManager
from strategies.random_strategy import RandomStrategy
from strategies.go_to_chest_strategy import GoToChestStrategy
from renderer import Renderer

# SERVER_IP = 'http://134.209.240.184:8081'
SERVER_IP = 'http://134.209.244.186:8081'
user_json = {'username': 'debelizonger', 'password': 'nafmWQarjy'}

train_url = 'http://134.209.240.184:1234/game?gameId=XX'


def play_game():
    token = server_communication.login(SERVER_IP, user_json)
    playerIdx, gameState = server_communication.join_game(SERVER_IP, token)

    start_game_state = json_parser.get_game_state_from_json(gameState, playerIdx)
    strategy_manager = StrategyManager()
    strategy_manager.current_strategy = GoToChestStrategy(strategy_manager)

    # make timeout for 15 seconds while waiting for response

    while True:
        gameStateParsed = json_parser.get_game_state_from_json(gameState, playerIdx)

        move = strategy_manager.execute_current_strategy(gameStateParsed)
        gameState = server_communication.game_make_move(SERVER_IP, token, move.json())

    print("------Game over!------")


def train_game():
    token = server_communication.login(SERVER_IP, user_json)
    server_communication.game_train(SERVER_IP, token, 'test1.txt', 0)
    game_state = server_communication.game_make_move_train(SERVER_IP, token, 'move', 0, 0)

    while True:
        # TODO: Implement our AI here
        action, q, r = 'move', 0, 0
        print(action, q, r)
        try:
            game_state = server_communication.game_make_move_train(SERVER_IP, token, action, q, r)
        except:
            print("Timeout error")
            break
    print("------Game over!------")


if __name__ == '__main__':
    # with open('json_example.json') as f:
        # js = json.load(f)
        # state = js['gameState']
        # # convert json to string
        # json_string = json.dumps(state)
        # game_state = json_parser.get_game_state_from_json(json_string, 1)
        #
        # renderer = Renderer(29, game_state.tiles, game_state.our_player)
        # renderer.render()
        # manager = StrategyManager()
        # manager.current_strategy = GoToChestStrategy(manager)
        # action = manager.execute_current_strategy(game_state)
        #
        # print(game_state.turn)
    play_game()
