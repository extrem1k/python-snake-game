import pytest

from engine.core import *


def test_initialize_game():
    state = initialize_game((10, 10))
    assert len(state["snake"]) == 1
    assert is_within_bounds(state["snake"][0], (10, 10))
    assert is_within_bounds(state["food"], (10, 10))
    assert state["snake"][0] != state["food"]


def test_move_object():
    assert move_object((5, 5), "up") == (5, 6)
    assert move_object((5, 5), "down") == (5, 4)
    assert move_object((5, 5), "left") == (4, 5)
    assert move_object((5, 5), "right") == (6, 5)


def test_check_collision():
    assert check_collision((1, 1), (1, 1)) is True
    assert check_collision((1, 1), (2, 2)) is False


def test_is_within_bounds():
    assert is_within_bounds((0, 0), (10, 10)) is True
    assert is_within_bounds((9, 9), (10, 10)) is True
    assert is_within_bounds((10, 10), (10, 10)) is False
    assert is_within_bounds((-1, 0), (10, 10)) is False


def test_update_game_state():
    state = initialize_game((5, 5))
    old_len = len(state["snake"])

    direction = state["direction"]
    state["food"] = move_object(state["snake"][0], direction)

    new_state = update_game_state(state, direction)

    assert len(new_state["snake"]) == old_len + 1
    assert not new_state["game_over"]
