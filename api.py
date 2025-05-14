from flask import Flask, jsonify, request
from flask_cors import CORS
from engine.core import initialize_game, update_game_state, render_board
from database.models import save_score, create_user
import uuid

app = Flask(__name__)
CORS(app)  # Włączenie CORS, aby frontend mógł komunikować się z API

# Słownik przechowujący stany gier użytkowników
game_states = {}


@app.route('/api/game/new', methods=['POST'])
def new_game():
    """
    Tworzy nową grę dla użytkownika
    """
    data = request.json
    nickname = data.get('nickname', 'Anonymous')
    board_size = data.get('board_size', (10, 10))

    # Tworzenie nowego użytkownika w bazie danych
    user_id = create_user(nickname, score=0)

    # Inicjalizacja gry
    state = initialize_game(board_size)

    # Generowanie unikalnego ID dla gry
    game_id = str(uuid.uuid4())

    # Zapisanie stanu gry w słowniku
    game_states[game_id] = {
        'state': state,
        'user_id': user_id,
        'nickname': nickname
    }

    # Konwersja stanu na format odpowiedni dla frontendu
    response_state = {
        'game_id': game_id,
        'board': render_board(state),
        'snake': state['snake'],
        'food': state['food'],
        'game_over': state['game_over'],
        'board_size': state['board_size'],
        'score': len(state['snake']) - 1
    }

    return jsonify(response_state)


@app.route('/api/game/state/<game_id>', methods=['GET'])
def get_game_state(game_id):
    """
    Pobiera aktualny stan gry
    """
    if game_id not in game_states:
        return jsonify({'error': 'Game not found'}), 404

    game_data = game_states[game_id]
    state = game_data['state']

    # Konwersja stanu na format odpowiedni dla frontendu
    response_state = {
        'board': render_board(state),
        'snake': state['snake'],
        'food': state['food'],
        'game_over': state['game_over'],
        'board_size': state['board_size'],
        'score': len(state['snake']) - 1
    }

    return jsonify(response_state)


@app.route('/api/game/move/<game_id>', methods=['POST'])
def move(game_id):
    """
    Wykonuje ruch w grze
    """
    if game_id not in game_states:
        return jsonify({'error': 'Game not found'}), 404

    direction = request.json.get('direction')
    if direction not in ['up', 'down', 'left', 'right']:
        return jsonify({'error': 'Invalid direction'}), 400

    game_data = game_states[game_id]
    state = game_data['state']

    # Sprawdzenie, czy próba ruchu w przeciwnym kierunku
    current_direction = state.get('direction', 'up')
    opposite_directions = {
        'up': 'down',
        'down': 'up',
        'left': 'right',
        'right': 'left'
    }

    # Zapobieganie zmianie na przeciwny kierunek
    if direction != opposite_directions[current_direction]:
        state['direction'] = direction

    # Aktualizacja stanu gry
    state = update_game_state(state, state['direction'])
    game_data['state'] = state

    # Sprawdzenie, czy gra się zakończyła
    if state['game_over']:
        # Zapis wyniku do bazy danych
        save_score(
            game_data['user_id'],
            state['board_size'],
            len(state['snake']) - 1,
            game_data['nickname']
        )

    # Konwersja stanu na format odpowiedni dla frontendu
    response_state = {
        'board': render_board(state),
        'snake': state['snake'],
        'food': state['food'],
        'game_over': state['game_over'],
        'board_size': state['board_size'],
        'score': len(state['snake']) - 1
    }

    return jsonify(response_state)


if __name__ == '__main__':
    app.run(debug=True, port=5000)