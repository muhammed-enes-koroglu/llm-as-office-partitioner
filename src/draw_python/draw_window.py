import matplotlib.pyplot as plt
import math


import path_helper
path_helper.add_project_path()

import importlib
import constants
import utils.utils_window as utils_window



importlib.reload(constants)
importlib.reload(utils_window)

def create_window(ax, window):
    # Suppose the window is in a wall. Create the window as a light gray line.
    # Window given as (x, y, size, orientation)
    x, y, window_size, orientation = window
    p1, p2 = utils_window.get_window_coordinates(x, y, window_size, orientation)
    
    # Teken de lijn (raam) tussen de twee punten
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=(0.82, 0.94, 0.98), linewidth=2)  # Light gray line



if __name__ == "__main__":
    fig, ax = plt.subplots()

    create_window(ax, (2, 3, 4, constants.ORIENTATION_UP))  # Stel x=2, y=3, window_size=4

    ax.set_aspect('equal')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    plt.grid(True)
    plt.show()
