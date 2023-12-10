import json

import game_state


def get_game_state_from_json(json_state, our_idx):
    turn = json_state['gameState']['turn']
    map_size = json_state['gameState']['map']['size']
    skull_win = json_state['gameState']['skullWin']
    tiles = [game_state.Tile(**tile) for sublist in json_state['gameState']['map']['tiles'] for tile in sublist]
    players = [game_state.Player(**player) for player in json_state['gameState']['scoreBoard']['players']]
    stone_attacks = [(tile['q'], tile['r']) for stone in json_state['gameState']['stones'] for tile in
                     json_state['gameState']['stones'][stone]['attackedTiles']]

    return game_state.GameState(turn, map_size, our_idx, skull_win, tiles, players, stone_attacks)


if __name__ == "__main__":
    json_example = json.load(open('json_example.json'))
    game_state = get_game_state_from_json(json_example, 1)
