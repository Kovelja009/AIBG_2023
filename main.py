import server_communication

SERVER_IP = 'http://134.209.240.184:8081'
# SERVER_IP = 'http://134.209.244.186:8081'


user_json = {'username': 'zonger', 'password': 'sifra'}
token = server_communication.login(SERVER_IP, user_json)
my_idx, game_state = server_communication.join_game(SERVER_IP, token)

while True:
    # TODO: Implement our AI here

    state =