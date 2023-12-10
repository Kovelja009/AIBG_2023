import json

import game_state


def get_game_state_from_json(json_state, our_idx):
    json_state = json.loads(json_state)
    turn = json_state['turn']
    map_size = json_state['map']['size']
    skull_win = json_state['skullWin']
    tiles = [game_state.Tile(**tile) for sublist in json_state['map']['tiles'] for tile in sublist]
    players = [game_state.Player(**player) for player in json_state['scoreBoard']['players']]
    stone_attacks = [(tile['q'], tile['r']) for stone in json_state['stones'] for tile in
                     json_state['stones'][stone]['attackedTiles']]

    return game_state.GameState(turn, map_size, our_idx, skull_win, tiles, players, stone_attacks)


if __name__ == "__main__":
    json_example = json.load(open('json_example.json'))
    game_state = get_game_state_from_json(json_example, 1)
