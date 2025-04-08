# engine/core.py
from typing import Tuple, List, Dict
import random

def initialize_game(board_size: Tuple[int, int]) -> dict:
    width, height = board_size
    initial_position = (width // 2, height // 2)
    food_position = generate_food_position([initial_position], board_size)
    return {
        "board_size": board_size,
        "snake": [initial_position],  # lista pozycji od głowy do ogona
        "direction": "up",
        "food": food_position,
        "game_over": False
    }

def move_object(position: Tuple[int, int], direction: str) -> Tuple[int, int]:
    x, y = position
    if direction == "up":
        return (x, y - 1)
    elif direction == "down":
        return (x, y + 1)
    elif direction == "left":
        return (x - 1, y)
    elif direction == "right":
        return (x + 1, y)
    else:
        raise ValueError("Invalid direction")

def check_collision(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
    return pos1 == pos2

def is_within_bounds(position: Tuple[int, int], board_size: Tuple[int, int]) -> bool:
    x, y = position
    width, height = board_size
    return 0 <= x < width and 0 <= y < height

def generate_food_position(snake: List[Tuple[int, int]], board_size: Tuple[int, int]) -> Tuple[int, int]:
    width, height = board_size
    empty_positions = [
        (x, y) for x in range(width) for y in range(height)
        if (x, y) not in snake
    ]
    return random.choice(empty_positions)

def update_game_state(state: dict, direction: str) -> dict:
    if not state["snake"]:
        state["game_over"] = True
        return state

    new_snake_head = move_object(state["snake"][0], direction)

    # Kolizja ze ścianą
    if not is_within_bounds(new_snake_head, state["board_size"]):
        state["game_over"] = True
        return state

    # Kolizja z samym sobą
    if new_snake_head in state["snake"]:
        state["game_over"] = True
        return state

    # Nowa głowa
    state["snake"].insert(0, new_snake_head)

    # Zjedzenie jedzenia
    if check_collision(new_snake_head, state["food"]):
        state["food"] = generate_food_position(state["snake"], state["board_size"])
        # NIE usuwamy ogona — wąż rośnie
    else:
        # Tylko jeśli długość > 1, usuwamy ogon
        if len(state["snake"]) > 1:
            state["snake"].pop()
        else:
            # Jeśli wąż miał tylko 1 segment – nie usuwaj, bo zniknie!
            pass

    return state

def render_board(state: dict) -> List[List[str]]:
    width, height = state["board_size"]
    board = [["." for _ in range(width)] for _ in range(height)]
    for idx, (x, y) in enumerate(state["snake"]):
        if 0 <= x < width and 0 <= y < height:
            board[y][x] = "O" if idx == 0 else "o"
    # Wstaw jedzenie
    fx, fy = state["food"]
    board[fy][fx] = "*"

    # Wstaw węża (głowa = O, reszta = o)
    for idx, (x, y) in enumerate(state["snake"]):
        if 0 <= x < width and 0 <= y < height:
            board[y][x] = "O" if idx == 0 else "o"

    return board