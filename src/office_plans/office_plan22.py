import path_helper
path_helper.add_project_path()

import constants
import utils.utils_desk as utils_desk

def define_office_plan():
    """ 
    Rectangle office (18 m × 18 m), 16 desks in 4×4 grid, 16 persons,
    8 disturbing persons (checker pattern), 2 doors, 2 windows, 2 circular objects.
    """
    office_coordinates = ('RECTANGLE', (18, 18))  # metres, SI

    # Doors
    door1 = ((0, 0), (0, 1), 80, constants.CLOCKWISE)
    door2 = ((18, 5), (18, 6), 170, constants.COUNTERCLOCKWISE)
    doors = [door1, door2]

    # Windows
    window1 = (0, 3, 13, constants.ORIENTATION_UP)
    window2 = (3, 18, 13, constants.ORIENTATION_RIGHT)
    windows = [window1, window2]

    # Desks & chairs: 4 rows × 4 columns
    rows = [3, 7, 11, 15]   # y‐positions (m)
    cols = [3, 7, 11, 15]   # x‐positions (m)
    desk_length = 2         # m
    desk_width  = 1         # m

    desks = []
    persons = []
    disturbing_persons = []

    for i, y in enumerate(rows):
        # First two rows face down, last two face up
        orientation = (
            constants.ORIENTATION_DOWN
            if i < 2
            else constants.ORIENTATION_UP
        )
        for j, x in enumerate(cols):
            desk = (x, y, orientation, desk_length, desk_width)
            desks.append(desk)

            chair = utils_desk.get_chair_coordinate(desk)
            persons.append(chair)

            # Checkerboard: every other seat is “disturbing”
            if (i + j) % 2 == 0:
                disturbing_persons.append(chair)

    # Two circular objects
    object1 = (constants.OBJECT_ROUND, (2, 5, 0.5))
    object2 = (constants.OBJECT_ROUND, (5, 5, 0.5))
    objects = [object1, object2]

    noise = []           # still empty
    moveable_walls = []  # still none

    return (
        office_coordinates,
        windows,
        doors,
        desks,
        persons,
        disturbing_persons,
        objects,
        noise,
        moveable_walls
    )
