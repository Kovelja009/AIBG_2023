import server_communication
import json_parser
from strategy_manager import StrategyManager
from strategies.go_to_chest_strategy import GoToChestStrategy
from game_utils import get_neighbouring_tiles
import random
from actions.move_action import MoveAction
from strategies.circle_stone_strategy import CircleStoneStrategy

SERVER_IP = 'http://134.209.244.186:8081'
user_json = {'username': 'debelizonger3', 'password': 'nafmWQarjy'}

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
