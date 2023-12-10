import server_communication
import json_parser

SERVER_IP = 'http://134.209.240.184:8081'
user_json = {'username': 'debelizonger4', 'password': 'nafmWQarjy'}

token = server_communication.login(SERVER_IP, user_json)
playerIdx, gameState = server_communication.join_game(SERVER_IP, token)
print(playerIdx, gameState)

while True:
    gameStateParsed = json_parser.get_game_state_from_json(gameState, playerIdx)
    q, r = gameStateParsed.our_player.position
    print(f"playerIdx: {playerIdx}, turn: {gameStateParsed.turn}, gameState: {gameStateParsed}, q: {q}, r: {r}")
    action = 'move'
    q += 1
    gameState = server_communication.game_make_move(SERVER_IP, token, action, q, r)
