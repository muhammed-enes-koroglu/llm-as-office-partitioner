import matplotlib.pyplot as plt


def point_person(ax, person):
    # Create a person as a green point. The person is given as (x, y).
    x, y = person
    ax.plot(x, y, marker='o', color='green', markersize=2)

def point_disturbing_person(ax, person):
    # Create a disturbing person by changing the point color to red.
    x, y = person
    ax.plot(x, y, marker='o', color='red', markersize=2)




if __name__ == "__main__":
    fig, ax = plt.subplots()

    point_person(ax, (1, 2))
    point_disturbing_person(ax, (2, 2))

    ax.set_aspect('equal')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    plt.grid(True)
    plt.show()
