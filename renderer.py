import matplotlib.pyplot as plt
from hexalattice.hexalattice import *
from game_state import EntityType, Tile, Player
from typing import Dict, Tuple

cell_colors = {
    EntityType.NONE: np.array([233, 236, 239]) / 255.0,
    EntityType.TREES: np.array([42, 157, 143]) / 255.0,
    EntityType.CHEST: np.array([244, 162, 97]) / 255.0,
    EntityType.STONE: np.array([173, 181, 189]) / 255.0,
    EntityType.CLIFF: np.array([52, 58, 64]) / 255.0,
    EntityType.ENEMY_PLAYER: np.array([188, 71, 73]) / 255.0,
    EntityType.SKULL: np.array([245, 66, 197]) / 255.0,
    EntityType.LEAVES: np.array([233, 196, 106]) / 255.0,
}

player_colors = {
    1: np.array([255, 0, 0]) / 255.0,
    2: np.array([255, 255, 0]) / 255.0,
    3: np.array([0, 255, 0]) / 255.0,
    4: np.array([0, 0, 255]) / 255.0,
}


class Renderer:
    board: List[List[Union[None,Tile]]]
    def __init__(self, board_size, tiles: Dict[Tuple[int, int], Tile], ourPlayer: Player):
        self.board_size = board_size
        self.plot_x_hex_coords = None
        self.plot_y_hex_coords = None
        self.first_plot_done = False
        self.plot_axis = plt.gca()
        self.board = []
        self.ourPlayer = ourPlayer

        # Fill board based on tiles (convert between coords)
        start_row_pos = (0, -(self.board_size // 2))
        col_cnt = self.board_size // 2 + 1
        for i in range(self.board_size // 2 + 1):
            self.board.append([])
            current_coord = start_row_pos
            for _ in range(self.board_size - col_cnt):
                self.board[-1].append(None)
            for _ in range(col_cnt):
                self.board[-1].append(tiles[current_coord])
                current_coord = (current_coord[0] + 1, current_coord[1])
            col_cnt += 1
            start_row_pos = (start_row_pos[0] - 1, start_row_pos[1] + 1)

        col_cnt -= 2
        start_row_pos = (-(self.board_size//2), 1)
        for _ in range(self.board_size//2):
            self.board.append([])
            current_coord = start_row_pos
            for _ in range(col_cnt):
                self.board[-1].append(tiles[current_coord])
                current_coord = (current_coord[0] + 1, current_coord[1])
            for _ in range(self.board_size - col_cnt):
                self.board[-1].append(None)

            col_cnt -= 1
            start_row_pos = (start_row_pos[0], start_row_pos[1] + 1)

        plt.ion()

    def display_legend(self):
        handles = []
        for key in cell_colors.keys():
            patch = mpatches.Patch(color=cell_colors[key], label=str(key))
            handles.append(patch)
        for key in player_colors.keys():
            patch = mpatches.Patch(color=player_colors[key], label=f'Player {key}')
            handles.append(patch)

        # Shrink current axis by 20%
        box = self.plot_axis.get_position()
        self.plot_axis.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        self.plot_axis.legend(loc='center left', bbox_to_anchor=(1, 0.5), handles=handles)

    def render(self):
        # ko zna sta sve ovo ispod radi ali izgleda da napravi hex grid
        rows_hex = [{} for _ in range(self.board_size)]
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] is not None:
                    if self.board[i][j].entity.type == EntityType.ENEMY_PLAYER or self.board[i][j].entity.type == EntityType.OUR_PLAYER:
                        rows_hex[i][(j - self.board_size // 4)] = player_colors[self.board[i][j].entity.playerIdx]
                    else:
                        rows_hex[i][(j - self.board_size // 4)] = cell_colors[self.board[i][j].entity.type]

        rows_rect = [[] for _ in range(self.board_size)]
        for i in range(self.board_size):
            col = -(i // 2)
            for _ in range(self.board_size):
                rows_rect[i].append(col)
                col += 1

        colors_board = np.ones((self.board_size, self.board_size, 3))
        for j in range(len(rows_rect)):
            row = rows_rect[j]
            for i in range(self.board_size):
                if row[i] in rows_hex[j]:
                    colors_board[j][i] = rows_hex[j][row[i]]

        colors_flat = np.full((self.board_size * self.board_size, 3), 0.5)
        j = 0
        for row in reversed(colors_board):
            for i in range(len(row)):
                colors_flat[j] = row[i]
                j += 1

        # Make new hex grid
        if not self.first_plot_done:
            hex_centers, _ = create_hex_grid(nx=self.board_size,
                                             ny=self.board_size,
                                             do_plot=False, h_ax=self.plot_axis)
            self.plot_x_hex_coords = hex_centers[:, 0]
            self.plot_y_hex_coords = hex_centers[:, 1]
            plt.show()
            self.first_plot_done = True

        plot_single_lattice_custom_colors(self.plot_x_hex_coords, self.plot_y_hex_coords,
                                          face_color=colors_flat,
                                          edge_color=colors_flat,
                                          min_diam=0.9,
                                          plotting_gap=0.05,
                                          rotate_deg=0, h_ax=self.plot_axis)

        self.display_legend()


