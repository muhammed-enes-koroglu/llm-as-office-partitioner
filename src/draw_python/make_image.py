
import matplotlib.pyplot as plt
import path_helper
path_helper.add_project_path()

import office_plans.office_plan as office_plan

import constants
from draw_python.draw import draw_office_plan

def create_image(ax, filename, office_coordinates):
    
    right_most = 0
    top_most = 0
    if office_coordinates[0] == constants.OFFICE_RECTANGLE:
        office_length, office_width = office_coordinates[1]
        right_most = office_length # highest x
        top_most = office_width # highest y
    
    if office_coordinates[0] == constants.OFFICE_POLYGON:
        right_most = max(office_coordinates[1], key=lambda p: p[0])[0] # highest x
        top_most = max(office_coordinates[1], key=lambda p: p[1])[1] # highest y

    
    # Plot instellingen
    ax.set_aspect('equal')
    ax.set_xlim(-3.2, right_most + 3.2)
    ax.set_ylim(-1, top_most + 1)

    # Achtergrond lichtgrijs
    ax.set_facecolor('#f0f0f0')  # Lichtgrijze kleur

    # Nummering uitschakelen
    ax.set_xticks([])  # Verwijder streepjes
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.legend(
    title='Iterations',
    loc='upper right',
    # frameon=True,
    fontsize=7,      # Klein lettertype voor inhoud
    title_fontsize=8 # Klein lettertype voor titel
)

    plt.savefig(filename, dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    
    office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, noise, moveable_walls = office_plan.define_office_plan()

    # Create figure
    fig, ax = plt.subplots()

    
    draw_office_plan(ax, office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, noise, moveable_walls, 0)
    create_image(ax, 'initial_offices/office_4.png', office_coordinates)

