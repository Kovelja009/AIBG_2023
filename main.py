import server_communication

SERVER_IP = 'http://134.209.240.184:8081'
# SERVER_IP = 'http://134.209.244.186:8081'
user_json = {'username': 'debelizonger1', 'password': 'nafmWQarjy'}


train_url = 'http://134.209.240.184:1234/game?gameId=XX'

def play_game():
    token = server_communication.login(SERVER_IP, user_json)
    my_idx, game_state = server_communication.join_game(SERVER_IP, token)

    # make timeout for 15 seconds while waiting for response

    while True:
        # TODO: Implement our AI here
        action, q, r = 'move', 0, 0
        try:
            game_state = server_communication.game_make_move(SERVER_IP, token, action, q, r, timeout=15)
        except:
            print("Timeout error")
            break
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
    # play_game()
    # train_game()
    server_communication.login(SERVER_IP, user_json)