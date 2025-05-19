
import path_helper
path_helper.add_project_path()

import importlib
import constants
import utils.utils_window as utils_window
import utils.utils_desk as utils_desk

importlib.reload(constants)
importlib.reload(utils_window)
importlib.reload(utils_desk)


def make_office_description_rectangle(office_length, office_width):
    office_description_rectangle = (f" The office is rectangular. It has a length of {office_length} "
        f"and a width of {office_width}. It is thereby defined by the 4 coordinates (0, 0), "
        f"({office_length}, 0), ({office_length}, {office_width}) and (0, {office_width}).")
    return office_description_rectangle

def make_office_description_polygon(coordinates):
    office_description_rectangle = f" The office has {len(coordinates)} walls that form a polygon. It is thereby defined by {len(coordinates)} coordinates that form a corner: "
    for i in range(0, len(coordinates)-1):
        x, y = coordinates[i]
        office_description_rectangle += f"({x},{y}), "
        
    x, y = coordinates[len(coordinates)-1]
    office_description_rectangle += f"({x},{y})."
    return office_description_rectangle

def make_window_description(windows):
    # Windows given as [(x, y, size, orientation),...]
    if len(windows) == 0:
        return ""
    basic_window_description = f" The walls contain {len(windows)} windows. Every window can be given by two coordinates [p1 and p2] that define the location and size in the grid. There is a window between "
    for i in range(0, len(windows)-1):
        window = windows[i]
        x, y, window_size, orientation = window
        p1, p2 = utils_window.get_window_coordinates_2d(x, y, window_size, orientation)
        basic_window_description += f"[{p1} and {p2}], "
        
    window = windows[len(windows)-1]
    x, y, window_size, orientation = window
    p1, p2 = utils_window.get_window_coordinates_2d(x, y, window_size, orientation)
    basic_window_description += f"[{p1} and {p2}]."
    return basic_window_description

def make_door_description(doors):
    # Doors given as [(hinge_coordinate, door_end_coordinate, opening_angle, rotation), ...]
    if len(doors) == 0:
        return ""
    basic_door_description = (f" The walls contain {len(doors)} doors. "
        "Every door can be given by a coordinate of the hinge, a coordinate of the other end of the door when closed, "
        "an angle that describes how far the door can open and the rotation of the door (clockwise or counterclockwise)."
        "This results in a representation as follows: [p1, p2, angle, rotation]. In the office, there is a door between ")
    for i in range(0, len(doors)-1):
        door = doors[i]
        p1, p2, angle, rotation = door
        basic_door_description += f"[{p1}, {p2}, {angle}, {rotation}], "
        
    door = doors[len(doors)-1]
    p1, p2, angle, rotation = door
    basic_door_description += f"[{p1}, {p2}, {angle}, {rotation}], "
    return basic_door_description


def make_desk_description_rectangle(desks):
    # Desks given as [(x, y, orientation, length, width),...]
    if len(desks) == 0:
        return ""
    basic_desk_description = (f" In the office are {len(desks)} desks with matching chairs. A desk is a rectangle and can be given by four coordinates [p1, p2, p3 and p4]. "
        "The matching chair is represented as a circle with a radius and center coordinate [r and p]. There is a desk at ")
    basic_chair_description = f" There is a chair at "
    for i in range(0, len(desks)-1):
        desk = desks[i]
        x, y, orientation, length, width = desk
        p1 = (x -length/2, y - width/2)
        p2 = (x + length/2, y - width/2)
        p3 = (x + length/2, y + width/2)
        p4 = (x - length/2, y + width/2)
        basic_desk_description += f"[{p1}, {p2}, {p3} and {p4}], "
        p = utils_desk.get_chair_coordinate(desk)
        basic_chair_description += f"[{constants.CHAIR_RADIUS} and {p}], "

    desk = desks[len(desks)-1]
    x, y, orientation, length, width = desk
    p1 = (x, y)
    p2 = (x + length, y)
    p3 = (x + length, y + width)
    p4 = (x, y + width)
    basic_desk_description += f"[{p1}, {p2}, {p3} and {p4}]."
    p = utils_desk.get_chair_coordinate(desk)
    basic_chair_description += f"[{constants.CHAIR_RADIUS} and {p}]."
    return basic_desk_description + basic_chair_description

def make_object_description(objects):
    # Objects given as [(type, type-info),...]
    if len(objects) == 0:
        return ""
    basic_object_description = (f" In the office can be some objects. These objects can have different forms: a rectangle, a circle or a polygon."
        f" A rectangular object is defined as [{constants.OBJECT_RECTANGLE}, p1, length, width], where p1 is the middle of the rectangle."
        f" A round object is defined as [{constants.OBJECT_ROUND}, p1, radius], where p1 is the middle of the circle."
        f" A polygon object is defined as [{constants.OBJECT_POLYGON}, [p1, p2, ...]]."
        " These are the following objects in the office: ")
    for i in range(0, len(objects)-1):
        object = objects[i]
        if object[0] == constants.OBJECT_RECTANGLE:
            basic_object_description += f"[{constants.OBJECT_RECTANGLE}, "
            x, y, length, width = object[1]
            basic_object_description += f"({x},{y}), {length}, {width}], "
        if object[0] == constants.OBJECT_ROUND:
            basic_object_description += f"[{constants.OBJECT_ROUND}, "
            x, y, radius = object[1]
            basic_object_description += f"({x},{y}), {radius}], "
        if object[0] == constants.OBJECT_POLYGON:
            coordinates = object[1]
            basic_object_description += f"[{constants.OBJECT_POLYGON}, ["
            for i in range(0, len(coordinates)-1):
                x, y = coordinates[i]
                basic_object_description += f"({x},{y}), "
            x, y = coordinates[len(coordinates)-1]
            basic_object_description += f"({x},{y})], "
            
    object = objects[len(objects)-1]
    if object[0] == constants.OBJECT_RECTANGLE:
        basic_object_description += f"[{constants.OBJECT_RECTANGLE}, "
        x, y, length, width = object[1]
        basic_object_description += f"({x},{y}), {length}, {width}]."
    if object[0] == constants.OBJECT_ROUND:
        basic_object_description += f"[{constants.OBJECT_ROUND}, "
        x, y, radius = object[1]
        basic_object_description += f"({x},{y}), {radius}]."
    if object[0] == constants.OBJECT_POLYGON:
        coordinates = object[1]
        basic_object_description += f"[{constants.OBJECT_POLYGON}, ["
        for i in range(0, len(coordinates)-1):
            x, y = coordinates[i]
            basic_object_description += f"({x},{y}), "
        x, y = coordinates[len(coordinates)-1]
        basic_object_description += f"({x},{y})]."
    return basic_object_description

def make_persons_description(persons):
    # Persons given as [(x,y), ...]
    if len(persons) == 0:
        return ""
    basic_persons_description = f" Currently there are {len(persons)} people working in the office. Every person is located at a coordinate: "
    for i in range(0, len(persons)-1):
        person = persons[i]
        x, y = person
        basic_persons_description += f"({x}, {y}), "
    
    person = persons[len(persons)-1]
    x, y = person
    basic_persons_description += f"({x}, {y})."
    return basic_persons_description

def make_disturbing_persons_description(disturbing_persons):
    # Disturbing_persons given as [(x,y), ...]

    if len(disturbing_persons) == 0:
        return ""
    basic_disturbing_persons_description = " There can however be some persons in the office that cause disturbance. Every person that causes disturbance is located at a coordinate: "
    for i in range(0, len(disturbing_persons)-1):
        person = disturbing_persons[i]
        x, y = person
        basic_disturbing_persons_description += f"({x}, {y}), "
    
    person = disturbing_persons[len(disturbing_persons)-1]
    x, y = person
    basic_disturbing_persons_description += f"({x}, {y})."
    return basic_disturbing_persons_description

def make_disturbing_points_description(disturbing_points):
    # disturbing_points given as [(x,y), ...]
    if len(disturbing_points) == 0:
        return ""
    basic_disturbing_points_description = " In the office are also some other points that cause disturbance. Every point that causes disturbance is located at a coordinate: "
    for i in range(0, len(disturbing_points)-1):
        disturbing_point = disturbing_points[i]
        x, y = disturbing_point
        basic_disturbing_points_description += f"({x}, {y}), "
    
    disturbing_point = disturbing_points[len(disturbing_points)-1]
    x, y = disturbing_point
    basic_disturbing_points_description += f"({x}, {y})."
    return basic_disturbing_points_description



def make_office_description(office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, disturbing_points):
    if office_coordinates[0] == constants.OFFICE_POLYGON:
        office_description = make_office_description_polygon(office_coordinates[1])
    else: 
        office_length, office_width = office_coordinates[1]
        office_description = make_office_description_rectangle(office_length, office_width)
    window_description = make_window_description(windows)
    door_description = make_door_description(doors)
    desk_description = make_desk_description_rectangle(desks)
    object_description = make_object_description(objects)
    persons_description = make_persons_description(persons)
    disturbing_persons_description = make_disturbing_persons_description(disturbing_persons)
    disturbing_points_description = make_disturbing_points_description(disturbing_points)
    return office_description + window_description + door_description + desk_description + object_description + persons_description + disturbing_persons_description + disturbing_points_description
