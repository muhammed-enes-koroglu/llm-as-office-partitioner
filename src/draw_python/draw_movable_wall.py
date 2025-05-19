
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.transforms as transforms

import path_helper
path_helper.add_project_path()

import importlib
import constants

importlib.reload(constants)


def create_movable_wall(ax, iteration_for_color_moveable_walls, label, x, y, angle, movable_wall_length=constants.MOVABLE_WALL_LENGTH, movable_wall_width=constants.MOVABLE_WALL_WIDTH):
    # Create a movable wall as a rectangle. Length for x-direction and width for y-direction.
    # X and y are the middle of the rectangle. The angle can be rotated using an angle in degrees.

    # Maak de rectangle gecentreerd op (x, y)
    if label:
        if iteration_for_color_moveable_walls == -1:
            rect = Rectangle((-movable_wall_length / 2, -movable_wall_width / 2),
                        movable_wall_length, movable_wall_width,
                        linewidth=1, edgecolor=constants.MOVEABLE_WALL_COLOR[iteration_for_color_moveable_walls % len(constants.MOVEABLE_WALL_COLOR)], facecolor='none', 
                        label='Final solution')
        else: rect = Rectangle((-movable_wall_length / 2, -movable_wall_width / 2),
                        movable_wall_length, movable_wall_width,
                        linewidth=1, edgecolor=constants.MOVEABLE_WALL_COLOR[iteration_for_color_moveable_walls % len(constants.MOVEABLE_WALL_COLOR)], facecolor='none', 
                        label=f'Iteration {iteration_for_color_moveable_walls}')
    else: 
        rect = Rectangle((-movable_wall_length / 2, -movable_wall_width / 2),
                        movable_wall_length, movable_wall_width,
                        linewidth=1, edgecolor=constants.MOVEABLE_WALL_COLOR[iteration_for_color_moveable_walls % len(constants.MOVEABLE_WALL_COLOR)], facecolor='none')

    # Apply translation + rotation
    t = transforms.Affine2D().rotate_deg(angle).translate(x, y) + ax.transData
    rect.set_transform(t)

    ax.add_patch(rect)




if __name__ == "__main__":
    fig, ax = plt.subplots()
    
    create_movable_wall(ax, True, 0, 0, 0, 30)

    ax.set_aspect('equal')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    plt.grid(True)
    plt.show()
