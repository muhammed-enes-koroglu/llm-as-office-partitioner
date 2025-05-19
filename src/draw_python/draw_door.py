import math

import matplotlib.pyplot as plt
from matplotlib.patches import Arc

import path_helper
path_helper.add_project_path()

import constants
import importlib
importlib.reload(constants)


def create_door(ax, hinge, door_end, opening_angle, rotation):
    # Create a door as a part of a circle. The coordinate hinge (x1,y1) is a fixed point.
    # The coordinate door_end (x2, y2) describes the other door end when closed. The opening angle tells how far the door can open. 
    x1, y1 = hinge
    x2, y2 = door_end

    door_length = math.dist(hinge, door_end)

    # Calculate angle of closed door
    delta_x = x2 - x1
    delta_y = y2 - y1
    start_angle = math.degrees(math.atan2(delta_y, delta_x))

    # Calculate point of maximal open door using clockwise or counterclockwise rotation
    if rotation == constants.CLOCKWISE:
        max_angle = start_angle - opening_angle
    else:
        max_angle = start_angle + opening_angle

    max_point = (x1 + door_length * math.cos(math.radians(max_angle)),
                 y1 + door_length * math.sin(math.radians(max_angle)))

    # Calculate point on arc
    point_on_curve_angle = (start_angle + max_angle) / 2
    point_on_curve = (x1 + door_length * math.cos(math.radians(point_on_curve_angle)),
                      y1 + door_length * math.sin(math.radians(point_on_curve_angle)))

    # Draw door
    ax.plot([x1, x2], [y1, y2], color='gray')  # closed door line
    ax.plot([x1, max_point[0]], [y1, max_point[1]], color='gray')  # open position line
    # ax.plot([x1, x2], [y1, y2], marker='o', linestyle='None', color='black')  # arc guide point

    # Add arc (door swing)
    arc_start = min(start_angle, max_angle)
    arc_extent = abs(opening_angle)
    ax.add_patch(Arc((x1, y1), 2 * door_length, 2 * door_length, angle=0,
                     theta1=arc_start, theta2=arc_start + arc_extent, color='gray', linestyle='dotted'))





if __name__ == "__main__":
    fig, ax = plt.subplots()

    create_door(ax, (1,1), (2,1), 170, constants.COUNTERCLOCKWISE)
    
    ax.set_aspect('equal')
    ax.set_xlim(-2, 4)
    ax.set_ylim(-2, 4)
    plt.grid(True)
    plt.show()
