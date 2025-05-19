
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
    description = {
        "shape": "rectangle",
        "office_length": office_length,
        "office_width": office_width,
        "corners": [(0, 0), (office_length, 0), (office_length, office_width), (0, office_width)]
    },
    return {"office_dimensions": description}

def make_office_description_polygon(coordinates):
    description = {
        "shape": "polygon",
        "corners": coordinates
    },
    return {"office_dimensions": description}

def make_window_description(windows):
    # Windows given as [(x, y, size, orientation),...]
    description = []
    for window in windows:
        x, y, window_size, orientation = window
        p1, p2 = utils_window.get_window_coordinates_2d(x, y, window_size, orientation)
        description.append({"start": p1, "end": p2})
    return {"windows": description}

def make_door_description(doors):
    # Doors given as [(hinge_coordinate, door_end_coordinate, opening_angle, rotation), ...]
    description = []
    for door in doors:
        p1, p2, angle, rotation = door
        description.append({
            "hinge": p1,
            "end": p2,
            "open_angle_degrees": angle,
            "rotation": rotation,
        })
    return {"doors": description}


def make_desk_description_rectangle(desks):
    # Desks given as [(x, y, orientation, length, width),...]
    description = []

    for desk in desks:
        x, y, orientation, length, width = desk
        p1 = (x -length/2, y - width/2)
        p2 = (x + length/2, y - width/2)
        p3 = (x + length/2, y + width/2)
        p4 = (x - length/2, y + width/2)
        description.append({"corners": [p1, p2, p3, p4]})
    return {"desks": description}

def make_chair_description(desks):
    description = []
    for desk in desks:
        x, y, orientation, length, width = desk
        p = utils_desk.get_chair_coordinate(desk)
        radius = constants.CHAIR_RADIUS
        description.append({"center": p, "radius": radius})
    return {"chairs": description}


def make_object_description(objects):
    # Objects given as [(type, type-info),...]
    description = []
    for object in objects:
        if object[0] == constants.OBJECT_RECTANGLE:
            x, y, length, width = object[1]
            description.append({"type": constants.OBJECT_RECTANGLE, "center": (x, y), "length": length, "width": width})
        if object[0] == constants.OBJECT_ROUND:
            x, y, radius = object[1]
            description.append({"type": constants.OBJECT_ROUND, "center": (x, y), "radius": radius})
        if object[0] == constants.OBJECT_POLYGON:
            coordinates = object[1]
            description.append({"type": constants.OBJECT_POLYGON, "corners": coordinates})
    return {"objects": description}

def make_persons_description(persons):
    # Persons given as [(x,y), ...]
    return {"present_persons": persons}

def make_disturbing_persons_description(disturbing_persons):
    # Disturbing_persons given as [(x,y), ...]
    return {"disturbing_persons": disturbing_persons}

def make_disturbing_points_description(disturbing_points):
    # disturbing_points given as [(x,y), ...]
    return {"disturbing_noises": disturbing_points}

def make_office_description(office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, disturbing_points):
    office_description = []
    if office_coordinates[0] == constants.OFFICE_POLYGON:
        office_description.append(make_office_description_polygon(office_coordinates[1]))
    else: 
        office_length, office_width = office_coordinates[1]
        office_description.append(make_office_description_rectangle(office_length, office_width))
    office_description.append(make_window_description(windows))
    office_description.append(make_door_description(doors))
    office_description.append(make_desk_description_rectangle(desks))
    office_description.append(make_chair_description(desks))
    office_description.append(make_object_description(objects))
    office_description.append(make_persons_description(persons))
    office_description.append(make_disturbing_persons_description(disturbing_persons))
    office_description.append(make_disturbing_points_description(disturbing_points)) 
    return {"office_description": office_description}
