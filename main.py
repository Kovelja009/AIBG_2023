import json

import server_communication
import json_parser
from strategy_manager import StrategyManager
from strategies.random_strategy import RandomStrategy
from strategies.go_to_chest_strategy import GoToChestStrategy
from renderer import Renderer
from game_utils import get_neighbouring_tiles
import random
from actions.move_action import MoveAction
from strategies.circle_stone_strategy import CircleStoneStrategy


def play_game():
    SERVER_IP = 'http://134.209.244.186:8081'
    user_json = {'username': 'debelizonger', 'password': 'nafmWQarjy'}

    token = server_communication.login(SERVER_IP, user_json)
    playerIdx, gameState = server_communication.join_game(SERVER_IP, token)
    print(playerIdx, gameState)

    start_game_state = json_parser.get_game_state_from_json(gameState, playerIdx)
    strategy_manager = StrategyManager()
    strategy_manager.current_strategy = CircleStoneStrategy(strategy_manager)

    while True:
        gameStateParsed = json_parser.get_game_state_from_json(gameState, playerIdx)
        q, r = gameStateParsed.our_player.position
        print(f"playerIdx: {playerIdx}, turn: {gameStateParsed.turn}, gameState: {gameStateParsed}, q: {q}, r: {r}")

        try:
            move = strategy_manager.execute_current_strategy(gameStateParsed)
        except:
            # Do random move
            print('Exception doing random move')
            playerTile = gameStateParsed.tiles[gameStateParsed.our_player.position]
            neighbors = get_neighbouring_tiles(gameStateParsed, playerTile)
            rand_move = random.choice(neighbors)
            move = MoveAction(rand_move.position)

        print(f'sending turn{gameStateParsed.turn} move: {move.json()}')

        gameState = server_communication.game_make_move(SERVER_IP, token, move.json())
        print('received new game state')


def train_game():
    SERVER_IP = 'http://134.209.244.186:8081'
    user_json = {'username': 'debelizonger', 'password': 'nafmWQarjy'}

    train_url = 'http://134.209.240.184:1234/game?gameId=XX'

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
    #     js = json.load(f)
    #     while True:
    #         state = js['gameState']
    #         # convert json to string
    #         json_string = json.dumps(state)
    #         game_state = json_parser.get_game_state_from_json(json_string, 1)
    #
    #         renderer = Renderer(29, game_state.tiles, game_state.our_player)
    #         renderer.update_state(game_state.tiles, game_state.our_player)
    #         renderer.render()
    #         manager = StrategyManager()
    #         manager.current_strategy = GoToChestStrategy(manager)
    #         action = manager.execute_current_strategy(game_state)
    #
    #         print(game_state.turn)
    play_game()
