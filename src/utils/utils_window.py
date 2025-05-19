import path_helper
path_helper.add_project_path()

import importlib
import constants

importlib.reload(constants)


def get_window_coordinates(x, y, window_size, orientation):
    p1 = (x, y, 0)
    if orientation == constants.ORIENTATION_UP:
        p2 = (x, y + window_size, 0)
    if orientation == constants.ORIENTATION_DOWN:
        p2 = (x, y - window_size, 0)
    if orientation == constants.ORIENTATION_RIGHT:
        p2 = (x + window_size, y, 0)
    if orientation == constants.ORIENTATION_LEFT:
        p2 = (x - window_size, y, 0)
    return p1, p2

def get_window_coordinates_2d(x, y, window_size, orientation):
    p1, p2 = get_window_coordinates(x, y, window_size, orientation)
    return (p1[0], p1[1]), (p2[0], p2[1])  # Remove z-coordinate