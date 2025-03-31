def move_object(position, direction):
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

def check_collision(pos1, pos2):
    return pos1 == pos2

def is_within_bounds(position, board_size):
    x, y = position
    max_x, max_y = board_size
    return 0 <= x < max_x and 0 <= y < max_y