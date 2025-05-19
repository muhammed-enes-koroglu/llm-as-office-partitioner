import path_helper
path_helper.add_project_path()

import importlib
import constants


importlib.reload(constants)

def get_chair_coordinate(desk):
    x, y, orientation, length, width = desk
    if orientation == constants.ORIENTATION_UP:
        return x,y + width/2 + 2*constants.CHAIR_RADIUS
    if orientation == constants.ORIENTATION_DOWN:
        return x ,y - width/2 - 2*constants.CHAIR_RADIUS
    if orientation == constants.ORIENTATION_LEFT:
        return x - length/2 - 2*constants.CHAIR_RADIUS, y
    if orientation == constants.ORIENTATION_RIGHT:
        return x + length/2 + 2*constants.CHAIR_RADIUS, y