import pytest
from game_engine.engine import move_object, check_collision, is_within_bounds

# Test dla move_object
def test_move_object_up():
    assert move_object((2, 2), "up") == (2, 1)

def test_move_object_left():
    assert move_object((2, 2), "left") == (1, 2)

def test_move_object_invalid_direction():
    with pytest.raises(ValueError):
        move_object((2, 2), "diagonal")

# Test dla check_collision
def test_check_collision_true():
    assert check_collision((3, 3), (3, 3)) == True

def test_check_collision_false():
    assert check_collision((3, 3), (4, 3)) == False

# Test dla is_within_bounds
def test_is_within_bounds_inside():
    assert is_within_bounds((3, 3), (10, 10)) == True

def test_is_within_bounds_outside():
    assert is_within_bounds((11, 3), (10, 10)) == False