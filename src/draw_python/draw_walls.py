import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

import path_helper
path_helper.add_project_path()

import importlib
import constants

importlib.reload(constants)

def create_wall(ax, x1, y1, x2, y2):
    # Create a wall as a line between two points.
    ax.plot([x1, x2], [y1, y2], color='black', linewidth=2)

def create_walls_rectangle(ax, x=0, y=0, office_length=constants.OFFICE_LENGTH, office_width=constants.OFFICE_WIDTH):
    # Create multiple walls as a rectangle.
    rectangle = Rectangle((x, y), office_length, office_width,
                          linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(rectangle)

def create_walls_polygon(ax, coordinates):
    # Create multiple walls as a polygon. Coordinates are given as [(x, y), ...].
    polygon = Polygon(coordinates, closed=True, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(polygon)



if __name__ == "__main__":
    fig, ax = plt.subplots()

    create_walls_rectangle(ax)
    # create_walls_polygon(ax, [(1, 1), (5, 1), (5, 4), (1, 4)])

    ax.set_aspect('equal')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    plt.grid(True)
    plt.show()
