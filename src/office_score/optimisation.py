import pretty_errors

import path_helper
path_helper.add_project_path()
from office_score.penalty_score import compute_office_penalty
from office_plans.office_plan import define_office_plan
from check_collisions import detect_all_collisions
import numpy as np
from scipy.optimize import basinhopping
import time

i = 0
def objective_function(params):
    """
    Objective function for the office layout problem.

    Parameters:
        params: A numpy array [x, y, angle] representing the movable wall's position.

    Returns:
        Negative heuristic score (because we want to maximize).
    """
    x, y, angle = params  # Unpack x, y, angle
    global i
    i += 1

    # Get the current office plan
    office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, dist_points, movable_walls = define_office_plan()

    # Instead of modifying moveable_walls in-place, create a new list
    movable_walls = movable_walls + [(x, y, angle)]  # This avoids modifying the original list

    # Check for collisions -> if there are any, return infinity
    if detect_all_collisions(movable_walls, office_coordinates, doors, desks, persons, objects):
        return np.inf
    
    # Compute the heuristic score
    score = compute_office_penalty(windows, persons, disturbing_persons, movable_walls)

    return score  # Negate because basinhopping minimizes by default

# Initial guess: (x, y, angle)
initial_guess = np.array([3.0, 3.0, 90.0])


# Run optimization
print("Starting optimization...")
start_time = time.time()
result = basinhopping(objective_function, initial_guess, niter=1000, stepsize=1.0, T=3)
end_time = time.time()

print(f"Optimization took {end_time - start_time:.2f} seconds")

# Get optimized coordinates
optimized_coords = result.x
print(f"Optimal coordinates: {optimized_coords[0]:.3f}, {optimized_coords[1]:.3f}, {optimized_coords[2]:.3f}")
print(f"Best heuristic value: {result.fun:.3f}")
print(f"Number of iterations: {i}")

from llm.llm_visualization import visualize_llm_solution
# Get the current office plan
office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, dist_points, movable_walls = define_office_plan()
visualize_llm_solution(-1, movable_walls + [(optimized_coords[0], optimized_coords[1], optimized_coords[2])])
