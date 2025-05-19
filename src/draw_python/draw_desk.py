import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

import path_helper
path_helper.add_project_path()

import math
import importlib
import constants
import utils.utils_desk as utils_desk

importlib.reload(constants)
importlib.reload(utils_desk)


def create_table(ax, x, y, length=constants.DESK_LENGTH, width=constants.DESK_WIDTH):
    # Create a table as a rectangle. Length for x-direction and width for y-direction.
    table = ax.add_patch(Rectangle((x-length/2, y-width/2), length, width, fill=False, edgecolor='black'))

def create_chair(ax, x, y, chair_radius=constants.CHAIR_RADIUS):
    # Create a chair as a circle.
    chair = ax.add_patch(Circle((x, y), chair_radius, fill=False, edgecolor='black'))

    # Add wheels to the chair.
    base_radius = constants.CHAIR_RADIUS + constants.WHEEL_RADIUS
    wheels = [
        ax.add_patch(
            Circle((
                x + base_radius * math.cos(i * (2 * math.pi / constants.NUMBER_OF_WHEELS)), 
                y + base_radius * math.sin(i * (2 * math.pi / constants.NUMBER_OF_WHEELS))
            ), constants.WHEEL_RADIUS, fill=False, edgecolor='black')
        )
        for i in range(constants.NUMBER_OF_WHEELS)
    ]

def create_desk(ax, desk):
    # Create a desk. A desk is given as (x, y, orientation, lenght, width).
    x, y, orientation, length, width = desk
    create_table(ax, x, y, length, width)
    x1, y1 = utils_desk.get_chair_coordinate(desk)
    create_chair(ax, x1, y1)




if __name__ == "__main__":
    fig, ax = plt.subplots()

    create_desk(ax, (1,1,constants.ORIENTATION_UP, 2, 1)) 

    ax.set_aspect('equal')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    plt.grid(True)
    plt.show()
