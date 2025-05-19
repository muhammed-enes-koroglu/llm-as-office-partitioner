import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle

import path_helper
path_helper.add_project_path()

import importlib
import constants
import utils.utils_desk as utils_desk

importlib.reload(constants)
importlib.reload(utils_desk)


def create_object_rectangle(ax, x, y, object_length, object_width):
    # Create an object as a rectangle. Length for x-direction and width for y-direction.
    # X and y are the middle of the rectangle.
    rectangle = Rectangle((x-object_length/2, y-object_width/2), object_length, object_width,
                          linewidth=1,  fill=False, edgecolor='black')
    ax.add_patch(rectangle)

def create_object_polygon(ax, coordinates):
    # Create an object as a polygon. Coordinates are given as [(x,y), ...].
    polygon = Polygon(coordinates, closed=True, fill=False, edgecolor='black')
    ax.add_patch(polygon)

def create_line(ax, x1, y1, x2, y2):
    # Create a line between two points.
    ax.plot([x1, x2], [y1, y2], color='black')

def create_object_round(ax, x, y, radius):
    # Create an object as a circle.
    circle = Circle((x, y), radius, fill=False, edgecolor='black')
    ax.add_patch(circle)




if __name__ == "__main__":
    fig, ax = plt.subplots()

    create_object_rectangle(ax, 0, 0, 4, 2)
    create_object_polygon(ax, [(1, 1), (4, 1), (4, 3), (1, 3)])
    create_line(ax, -2, -2, 2, 2)
    create_object_round(ax, 0, 4, 1)

    ax.set_aspect('equal')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    plt.grid(True)
    plt.show()
