import path_helper
path_helper.add_project_path()

import constants
import utils.utils_desk as utils_desk

def define_office_plan():
    """ 
    Polygon office, 3 persons and 3 desks, 1 disturbing person, 1 doors, 2 windows.

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

    office_coordinates = (constants.OFFICE_POLYGON, [(0,0), (0,10), (8,10), (8,5), (4,5), (4,0)])

    window1 = (0, 3, 5, constants.ORIENTATION_UP)
    window2 = (1, 10, 6, constants.ORIENTATION_RIGHT)
    windows = [window1, window2]

    door1 = ((0,0.5), (0,1.5), 120, constants.CLOCKWISE)
    doors = [door1]


    desk_length = 2 
    desk_width = 1
    desk1 = (2,3,constants.ORIENTATION_DOWN, desk_length, desk_width)
    desk2 = (2,7,constants.ORIENTATION_UP, desk_length, desk_width)
    desk3 = (6,7,constants.ORIENTATION_UP, desk_length, desk_width)
    desks = [desk1, desk2, desk3]

    person1 = utils_desk.get_chair_coordinate(desk1)
    person2 = utils_desk.get_chair_coordinate(desk2)
    person3 = utils_desk.get_chair_coordinate(desk3)
    persons = [person1, person2, person3]
    
    disturbing_person1 = person1
    disturbing_persons = [disturbing_person1]

    objects = []

    noise = []

    moveable_walls = []

    # moveable_wall1 = (4,2, 90)
    # moveable_wall2 = (3,5,0)
    # moveable_wall3 = (3.5,4,-45)
    # moveable_walls = [moveable_wall1, moveable_wall2, moveable_wall3]

    return office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, noise, moveable_walls
