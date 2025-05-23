import os
import time

import keyboard

from database.models import create_user
from engine.core import initialize_game, render_board, update_game_state

DIRECTION_KEYS = {"w": "up", "s": "down", "a": "left", "d": "right"}


def get_input():
    for key, direction in DIRECTION_KEYS.items():
        if keyboard.is_pressed(key):
            return direction
    return None


def print_board(board):
    # Wyświetlanie planszy od najwyższego Y (układ kartezjański)
    for row in reversed(board):
        print(" ".join(row))


def get_board_size():
    while True:
        try:
            width = int(input("Podaj szerokość planszy (5-25): "))
            height = int(input("Podaj wysokość planszy (5-25): "))
            if 5 <= width <= 25 and 5 <= height <= 25:
                return (width, height)
            else:
                print("Rozmiary muszą być w zakresie od 5 do 25.")
        except ValueError:
            print("Wprowadź liczby całkowite.")


def run_game():
    print("Rejestracja użytkownika...")
    nickname = input("Podaj swój nickname: ")
    print(f"Podany nickname: {nickname}")

    # 🔥 Nowe: zapytaj o rozmiar planszy od użytkownika:
    board_size = get_board_size()

    # 🛠️ Poprawione: przekazujemy nickname i score (0 na start)
    user_id = create_user(nickname, score=0)
    print("Zarejestrowano gracza, id:", user_id)

    # 🔥 Nowe: przekazujemy rozmiar planszy do gry
    state = initialize_game(board_size)
    direction = "right"

    # Rejestracja czasu rozpoczęcia gry
    start_time = time.time()
    step_delay = 0.2
    last_move_time = time.time()

    while not state.get("game_over"):
        os.system("cls" if os.name == "nt" else "clear")
        board = render_board(state)
        print_board(board)
        print("Sterowanie: W (góra), A (lewo), S (dół), D (prawo)")

        new_direction = get_input()
        if new_direction:
            # Zapobiegamy natychmiastowej zmianie na przeciwny kierunek
            opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
            if new_direction != opposite[direction]:
                direction = new_direction

        current_time = time.time()
        if current_time - last_move_time >= step_delay:
            state = update_game_state(state, direction)
            last_move_time = current_time

        time.sleep(0.01)  # Krótka pauza zmniejszająca zużycie CPU

    # Po zakończeniu gry:
    end_time = time.time()
    play_time = end_time - start_time

    # Przykładowe obliczenie wyniku: długość węża minus 1 (na podstawie logiki gry)
    final_score = len(state["snake"]) - 1
    from database.models import save_score

    save_score(user_id, state["board_size"], final_score, nickname)

    print("Gra zakończona!")
    print("Wynik gry:", final_score)
    print("Czas gry: {:.2f} sekund".format(play_time))
    print("Wynik zapisany w bazie danych.")


if __name__ == "__main__":
    run_game()
