import path_helper
path_helper.add_project_path()

import constants
import utils.utils_desk as utils_desk

def define_office_plan():
    """ 
    Rectangle office, 2 persons and desks, 1 disturbing person, 1 door, 1 window, 1 noise point object.

    Define the office plan with windows, desks, persons, disturbing persons, and movable walls.
    Returns the lists of objects for drawing and collision detection.
    
    Returns:
        office_plan: Tuple of lists (windows, desks, persons, disturbing_persons, moveable_walls)
        
        windows: List of window tuples (x, y, size, orientation)

        doors: List of door tuples (hinge_coordinates, door_end_coordinates, opening_angle, rotation)
        
        desks: List of desk tuples (x, y, orientation, length, width)
        
        persons: List of person tuples (x, y)
        
        disturbing_persons: List of disturbing person tuples (x, y)
        
        objects: List of objects (object_type, object_additional_info)

        disturbing_points: List of disturbing points tuples (x,y)
        
        moveable_walls: List of movable wall tuples (x, y, angle)
    """

    office_coordinates = ('RECTANGLE', (8,5))

    window1 = (1, 5, 6, constants.ORIENTATION_RIGHT)
    windows = [window1]

    door1 = ((4,0), (5,0), 170, constants.COUNTERCLOCKWISE)
    doors = [door1]


    desk_length = 1
    desk_width = 2
    desk1 = (2.5,2.5,constants.ORIENTATION_LEFT, desk_length, desk_width)
    desk2 = (5.5,2.5,constants.ORIENTATION_RIGHT, desk_length, desk_width)
    desks = [desk1, desk2]

    person1 = utils_desk.get_chair_coordinate(desk1)
    person2 = utils_desk.get_chair_coordinate(desk2)
    persons = [person1, person2]
    
    disturbing_person1 = person1
    disturbing_persons = [disturbing_person1]

    object1 = (constants.OBJECT_RECTANGLE, (4, 4, 0.5, 0.5))
    objects = [object1]

    noise1 = (4,4)
    noise = [noise1]

    moveable_walls = []

    # moveable_wall2 = (3,5,0)
    # moveable_wall3 = (3.5,4,-45)
    # moveable_walls = [moveable_wall1, moveable_wall2, moveable_wall3]

    return office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, noise, moveable_walls
