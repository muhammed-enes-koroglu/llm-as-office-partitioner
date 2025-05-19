
import matplotlib.pyplot as plt

import path_helper
path_helper.add_project_path()


# This noise function is only used for none-persons. Noisy persons can be drawn with draw_person.py
def point_noise(ax, noise):
    # Create noise as a blue point. The noise is given as (x,y).
    x, y = noise
    ax.plot(x, y, marker='o', color='blue', markersize=2)



if __name__ == "__main__":
    fig, ax = plt.subplots()

    point_noise(ax, (1, 2))

    ax.set_aspect('equal')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    plt.grid(True)
    plt.show()
