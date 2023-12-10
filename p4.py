import server_communication
import json_parser
from strategy_manager import StrategyManager
from strategies.random_strategy import RandomStrategy


SERVER_IP = 'http://134.209.244.186:8081'
user_json = {'username': 'debelizonger4', 'password': 'nafmWQarjy'}

token = server_communication.login(SERVER_IP, user_json)
playerIdx, gameState = server_communication.join_game(SERVER_IP, token)
print(playerIdx, gameState)

start_game_state = json_parser.get_game_state_from_json(gameState, playerIdx)
strategy_manager = StrategyManager(RandomStrategy(start_game_state))

while True:
    gameStateParsed = json_parser.get_game_state_from_json(gameState, playerIdx)
    q, r = gameStateParsed.our_player.position
    print(f"playerIdx: {playerIdx}, turn: {gameStateParsed.turn}, gameState: {gameStateParsed}, q: {q}, r: {r}")

    move = strategy_manager.execute_current_strategy(gameStateParsed)
    gameState = server_communication.game_make_move(SERVER_IP, token, move.json())
