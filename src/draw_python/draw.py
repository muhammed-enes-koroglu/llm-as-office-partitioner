import path_helper
path_helper.add_project_path()

import math
import importlib
import constants
import draw_python.draw_desk as draw_desk
import draw_python.draw_walls as draw_walls
import draw_python.draw_movable_wall as draw_movable_wall
import draw_python.draw_window as draw_window
import draw_python.draw_door as draw_door
import draw_python.draw_object as draw_object
import office_description.office_to_text as office_to_text
import utils.utils_desk as utils_desk
import draw_python.draw_person as draw_person
#import check_collisions
import office_plans.office_plan as office_plan
import draw_python.draw_noise as draw_noise
import matplotlib.pyplot as plt

# Forceer het opnieuw laden van de module
importlib.reload(constants)
importlib.reload(draw_desk)
importlib.reload(draw_walls)
importlib.reload(draw_movable_wall)
importlib.reload(draw_window)
importlib.reload(office_to_text)
importlib.reload(utils_desk)
importlib.reload(draw_person)
importlib.reload(office_plan)
importlib.reload(draw_door)
importlib.reload(draw_object)
importlib.reload(draw_noise)


def draw_office_plan(ax, office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, noise, moveable_walls, iteration_for_color_moveable_walls):

    if office_coordinates[0] == constants.OFFICE_RECTANGLE:
        office_length, office_width = office_coordinates[1]
        draw_walls.create_walls_rectangle(ax, office_length=office_length, office_width=office_width)
    
    if office_coordinates[0] == constants.OFFICE_POLYGON:
        draw_walls.create_walls_polygon(ax, office_coordinates[1])  

    for window in windows:
        draw_window.create_window(ax, window)

    for door in doors:
        draw_door.create_door(ax, *door)

    for desk in desks:
        draw_desk.create_desk(ax, desk)

    for person in persons:
        draw_person.point_person(ax, person)

    for person in disturbing_persons:
        draw_person.point_disturbing_person(ax, person)

    for object in objects:
        if object[0] == constants.OBJECT_RECTANGLE:
            draw_object.create_object_rectangle(ax, *object[1])
        if object[0] == constants.OBJECT_POLYGON:
            draw_object.create_object_polygon(ax, object[1])
        if object[0] == constants.OBJECT_ROUND:
            draw_object.create_object_round(ax, *object[1])

    for noise_point in noise:
        draw_noise.point_noise(ax, noise_point)
        
    first = True
    for moveable_wall in moveable_walls:
        draw_movable_wall.create_movable_wall(ax, iteration_for_color_moveable_walls, first, *moveable_wall)
        first = False  # Alleen de eerste krijgt label=True






if __name__ == "__main__":
    
    office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, noise, moveable_walls = office_plan.define_office_plan()

    
    # Create figure
    fig, ax = plt.subplots()

    # moveable_walls +=  [(3.8, 2, 90), (3.8, 16, 90)]
    draw_office_plan(ax, office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, noise, moveable_walls, 0)
    
    # Plot instellingen
    ax.set_aspect('equal')
    ax.set_xlim(-2, 20)
    ax.set_ylim(-2, 20)

    # Achtergrond lichtgrijs
    ax.set_facecolor('#f0f0f0')  # Lichtgrijze kleur

    # Nummering uitschakelen
    ax.set_xticks([])  # Verwijder streepjes
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    plt.show()
