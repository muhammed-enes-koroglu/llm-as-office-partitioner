import path_helper
path_helper.add_project_path()

import constants
import utils.utils_desk as utils_desk

def define_office_plan():
    """ 
    Polygon office, 3 persons and 3 desks, 1 disturbing person, 1 doors, 1 window, 1 rectangular object.

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

    office_coordinates = (constants.OFFICE_POLYGON, [(0,0), (2,10), (8,10), (6,0)])

    window1 = (3, 10, 4, constants.ORIENTATION_RIGHT)
    windows = [window1]

    door1 = ((1,0), (2,0), 160, constants.COUNTERCLOCKWISE)
    doors = [door1]


    desk1_length = 1
    desk1_width = 2
    desk2_length = 2
    desk2_width = 1
    desk1 = (3.5,7,constants.ORIENTATION_LEFT, desk1_length, desk1_width)
    desk2 = (5.5,7,constants.ORIENTATION_RIGHT, desk1_length, desk1_width)
    desk3 = (4,4,constants.ORIENTATION_DOWN, desk2_length, desk2_width)
    desks = [desk1, desk2, desk3]

    person1 = utils_desk.get_chair_coordinate(desk1)
    person2 = utils_desk.get_chair_coordinate(desk2)
    person3 = utils_desk.get_chair_coordinate(desk3)
    persons = [person1, person2, person3]
    
    disturbing_person1 = person1
    disturbing_persons = [disturbing_person1]

    
    object1 = (constants.OBJECT_RECTANGLE, (4.5, 1, 2, 1))
    objects = [object1]

    noise = []

    moveable_walls = []

    # moveable_wall1 = (4,2, 90)
    # moveable_wall2 = (3,5,0)
    # moveable_wall3 = (3.5,4,-45)
    # moveable_walls = [moveable_wall1, moveable_wall2, moveable_wall3]

    return office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, noise, moveable_walls
