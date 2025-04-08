import time
import os

import keyboard

from engine.core import initialize_game, update_game_state, render_board

DIRECTION_KEYS = {
    'w': 'up',
    's': 'down',
    'a': 'left',
    'd': 'right'
}

def get_input():
    for key, direction in DIRECTION_KEYS.items():
        if keyboard.is_pressed(key):
            return direction
    return None

def print_board(board):
    for row in board:
        print(" ".join(row))


def run_game():
    import time
    import os

    state = initialize_game((10, 10))
    direction = 'right'

    step_delay = 0.2  # jak często porusza się wąż
    last_move_time = time.time()

    while not state.get("game_over"):
        os.system('cls' if os.name == 'nt' else 'clear')
        board = render_board(state)
        print_board(board)
        print("Sterowanie: W (góra), A (lewo), S (dół), D (prawo)")

        # 🔁 sprawdzaj input co chwila
        new_direction = get_input()
        if new_direction:
            opposite = {
                'up': 'down',
                'down': 'up',
                'left': 'right',
                'right': 'left'
            }
            if new_direction != opposite[direction]:
                direction = new_direction

        # 🔁 tylko co step_delay przesuwaj węża
        current_time = time.time()
        if current_time - last_move_time >= step_delay:
            state = update_game_state(state, direction)
            last_move_time = current_time

        time.sleep(0.01)  # szybka pętla, mały odpoczynek dla CPU

    print("Game Over!")