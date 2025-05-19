import pretty_errors

import path_helper
path_helper.add_project_path()

import math
from office_score.check_collisions import get_rectangle_polygon, segments_intersect
import constants
from utils import utils_window
from office_plans.office_plan import define_office_plan
import time

def compute_office_penalty(windows: list, persons: list, disturbing_persons: list, moveable_walls: list, 
                           alpha:float=10, beta:float=0.5, gamma:float=0.5) -> float:
    """
    Computes a penalty score for an office layout to evaluate its quality.

    This function calculates a score to measure how optimal an office layout is.
    A higher score indicates a less favorable configuration, while a lower score
    indicates a more comfortable and efficient arrangement.

    The penalty calculation considers three key factors:
        1. Disturbance from disruptive individuals.
        2. Visibility of windows.
        3. Visibility between non-disruptive individuals.

    Args:
        windows (list): A list of window tuples (x, y, size, orientation), defining the location, size, and orientation of each window. Orientation can be one of: 'UP', 'DOWN', 'LEFT', 'RIGHT'
        persons (list): A list of tuples (x, y), representing the positions of people in the office.
        disturbing_persons (list): A list of tuples (x, y), representing the positions of disturbing individuals.
        moveable_walls (list): A list of tuples (x, y, angle), representing movable walls within the office space. The moveable wall is rotated around the center point (x, y) by the given angle in degrees. An angle of 0 degrees means the wall is aligned with the x-axis.
        alpha (float, optional): Weight for penalizing disturbing exposure. Default is 10.
        beta (float, optional): Weight for rewarding window visibility. Default is 0.5.
        gamma (float, optional): Weight for rewarding visibility between people. Default is 0.5.

    Returns:
        float: The computed penalty score. Lower values indicate better office arrangements.
    
    Example:
        >>> windows = [(0, 3, 5, 'UP'), (1, 10, 6, 'RIGHT')]
        >>> persons = [(1, 2), (5, 2), (1, 6), (5, 6)]
        >>> disturbing_persons = [(1, 2)]
        >>> moveable_walls = [(3, 2, 90), (1.5, 5, 0), (2.5, 4, -45)]
        >>> score = compute_office_penalty(windows, persons, disturbing_persons, moveable_walls)
        >>> print(f"Penalty Score: {score}")
    """

    a, b, c = compute_separate_penalties(windows, persons, disturbing_persons, moveable_walls, alpha, beta, gamma)
    # Combine the penalties into a single score.
    # The three penalties are already weighted by their respective alpha, beta, and gamma values.
    # The final score is the sum of these penalties.
    # The lower the score, the better the office arrangement.
    penalty_score = a + b + c
    return penalty_score    

def compute_separate_penalties(windows: list, persons: list, disturbing_persons: list, moveable_walls: list, 
                           alpha:float=10, beta:float=0.5, gamma:float=0.5) -> tuple[float, float, float]:
    """
    Computes the penalty scores for an office layout to evaluate its quality.

    This function calculates the scores to measure how optimal an office layout is.
    A higher score indicates a less favorable configuration, while a lower score
    indicates a more comfortable and efficient arrangement.

    The penalty calculation considers three key factors:
        1. Disturbance from disruptive individuals.
        2. Visibility of windows.
        3. Visibility between non-disruptive individuals.

    Args:
        windows (list): A list of window tuples (x, y, size, orientation), defining the location, size, and orientation of each window. Orientation can be one of: 'UP', 'DOWN', 'LEFT', 'RIGHT'
        persons (list): A list of tuples (x, y), representing the positions of people in the office.
        disturbing_persons (list): A list of tuples (x, y), representing the positions of disturbing individuals.
        moveable_walls (list): A list of tuples (x, y, angle), representing movable walls within the office space. The moveable wall is rotated around the center point (x, y) by the given angle in degrees. An angle of 0 degrees means the wall is aligned with the x-axis.
        alpha (float, optional): Weight for penalizing disturbing exposure. Default is 10.
        beta (float, optional): Weight for rewarding window visibility. Default is 0.5.
        gamma (float, optional): Weight for rewarding visibility between people. Default is 0.5.

    Returns:
        tuple[float, float, float]: The computed penalty scores, containing: exposure_to_disturbing_people, exposure_to_windows, exposure_to_non_disturbing. Lower values indicate better office arrangements.
    
    Example:
        >>> windows = [(0, 3, 5, 'UP'), (1, 10, 6, 'RIGHT')]
        >>> persons = [(1, 2), (5, 2), (1, 6), (5, 6)]
        >>> disturbing_persons = [(1, 2)]
        >>> moveable_walls = [(3, 2, 90), (1.5, 5, 0), (2.5, 4, -45)]
        >>> scores = compute_separate_penalties(windows, persons, disturbing_persons, moveable_walls)
        >>> print(f"Penalty Score: {scores}")
    """
    epsilon = 1e-6  # To avoid division by zero
    penalty = 0.0
    # Blockers used in most checks (including office walls)
    blockers_all = compute_office_blockers(moveable_walls, include_office=True)
    # For window checks, ignore the office walls to avoid false blocking.
    blockers_no_office = compute_office_blockers(moveable_walls, include_office=False)
    
    # Sampling parameters
    person_sample_count = 16         # number of sample points around a person
    person_sample_radius = .5        # radius for person sampling (in SI units)
    window_sample_count = 8           # number of sample points along a window

    # 1. Penalize exposure to disturbing persons.
    exposure_to_disturbing_people = calculate_exposure_to_disturbing_people(persons, disturbing_persons, alpha, epsilon, blockers_all, person_sample_count, person_sample_radius)
    
    # 2. Reward exposure to windows.
    exposure_to_windows = calculate_exposure_to_windows(windows, persons, beta, epsilon, blockers_no_office, person_sample_count, person_sample_radius, window_sample_count)
    
    # 3. Reward visibility among non-disturbing persons.
    exposure_to_non_disturbing = calculate_exposure_to_friendlies(persons, disturbing_persons, gamma, epsilon, blockers_all, person_sample_count, person_sample_radius)
    
    return exposure_to_disturbing_people, exposure_to_windows, exposure_to_non_disturbing

def calculate_exposure_to_disturbing_people(persons, disturbing_persons, alpha, epsilon, blockers_all, person_sample_count, person_sample_radius):
    exposure_to_disturbing_persons = 0
    for p in persons:
        p_samples = generate_sample_points_around(p, person_sample_radius, person_sample_count)
        for d in disturbing_persons:
            # Skip if the person is the same as the disturbing person.
            if p == d:
                continue
            d_samples = generate_sample_points_around(d, person_sample_radius, person_sample_count)
            visibility = fraction_visible(p_samples, d_samples, blockers_all)
            dist = euclidean_distance(p, d)
            # The closer the disturbing person and the higher the visible fraction, the larger the penalty.
            exposure_to_disturbing_persons += alpha * visibility / (dist + epsilon)
    return exposure_to_disturbing_persons

def calculate_exposure_to_windows(windows, persons, beta, epsilon, blockers_no_office, person_sample_count, person_sample_radius, window_sample_count):
    exposure_to_windows = 0
    for p in persons:
        p_samples = generate_sample_points_around(p, person_sample_radius, person_sample_count)
        for window in windows:
            # Get window endpoints and sample along the window.
            p1, p2 = utils_window.get_window_coordinates_2d(window[0], window[1], window[2], window[3])
            window_samples = sample_points_along_line(p1, p2, window_sample_count)
            visibility = fraction_visible(p_samples, window_samples, blockers_no_office)
            # Use window midpoint for distance computation.
            mid = window_midpoint(window)
            dist = euclidean_distance(p, mid)
            # The closer the window and the more visible it is, the higher the benefit.
            exposure_to_windows -= beta * visibility / (dist + epsilon)**2
    return exposure_to_windows

def calculate_exposure_to_friendlies(persons, disturbing_persons, gamma, epsilon, blockers_all, person_sample_count, person_sample_radius):
    non_disturbing = [p for p in persons if p not in disturbing_persons]
    n = len(non_disturbing)
    exposure_to_non_disturbing = 0
    for i in range(n):
        for j in range(i + 1, n):
            p = non_disturbing[i]
            q = non_disturbing[j]
            p_samples = generate_sample_points_around(p, person_sample_radius, person_sample_count)
            q_samples = generate_sample_points_around(q, person_sample_radius, person_sample_count)
            visibility = fraction_visible(p_samples, q_samples, blockers_all)
            dist = euclidean_distance(p, q)
            exposure_to_non_disturbing -= gamma * visibility / (dist + epsilon)**2
    return exposure_to_non_disturbing

# Helper functions
def euclidean_distance(p, q):
    """Return the Euclidean distance between two points p and q."""
    return math.hypot(p[0] - q[0], p[1] - q[1])

def generate_sample_points_around(center, radius, count):
    """
    Generate `count` points evenly distributed in a circle of given radius around the center.
    This is used for sampling around a person's location.
    """
    x, y = center
    pts = []
    for i in range(count):
        angle = 2 * math.pi * i / count
        pts.append((x + radius * math.cos(angle), y + radius * math.sin(angle)))
    return pts

def sample_points_along_line(p1, p2, count):
    """
    Generate `count` equally spaced points along the line segment between p1 and p2.
    This is used for sampling along the window.
    """
    pts = []
    if count < 2:
        return [((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)]
    for i in range(count):
        t = i / (count - 1)
        pts.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
    return pts

def is_blocked(a, b, blockers):
    """
    Returns True if the segment from a to b is blocked by any segment in blockers.
    """
    for seg in blockers:
        if segments_intersect(a, b, seg[0], seg[1]):
            return True
    return False

def fraction_visible(sample_points_a, sample_points_b, blockers):
    """
    Compute the fraction of rays from sample_points_a to sample_points_b that are unblocked.
    Returns a value between 0.0 (fully blocked) and 1.0 (completely unobstructed).
    """
    total = len(sample_points_a) * len(sample_points_b)
    unblocked = 0
    for a in sample_points_a:
        for b in sample_points_b:
            if not is_blocked(a, b, blockers):
                unblocked += 1
    return unblocked / total

def window_midpoint(window):
    """
    Given a window tuple (x, y, window_size, orientation), return the midpoint.
    (This is still used for distance computation.)
    """
    p1, p2 = utils_window.get_window_coordinates_2d(window[0], window[1], window[2], window[3])
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def compute_office_blockers(moveable_walls, include_office=True):
    """
    Compute a list of line segments (each as ((x1, y1), (x2, y2))) that block line-of-sight.
    """
    blockers = []
    if include_office:
        # Office walls defined as a rectangle
        office_walls = [
            ((0, 0), (constants.OFFICE_LENGTH, 0)),
            ((constants.OFFICE_LENGTH, 0), (constants.OFFICE_LENGTH, constants.OFFICE_WIDTH)),
            ((constants.OFFICE_LENGTH, constants.OFFICE_WIDTH), (0, constants.OFFICE_WIDTH)),
            ((0, constants.OFFICE_WIDTH), (0, 0))
        ]
        blockers.extend(office_walls)
    # Add movable wall segments.
    for mw in moveable_walls:
        poly = get_rectangle_polygon(mw[0], mw[1], constants.MOVABLE_WALL_LENGTH, constants.MOVABLE_WALL_WIDTH, mw[2])
        n = len(poly)
        for i in range(n):
            p1 = poly[i]
            p2 = poly[(i + 1) % n]
            blockers.append(((p1[0], p1[1]), (p2[0], p2[1])))
    return blockers

def line_of_sight(p, q, blockers):
    """
    Returns True if the line segment from point p to q is not blocked by any segment in blockers.
    (This remains for quick binary checks if needed.)
    """
    for seg in blockers:
        if segments_intersect(p, q, seg[0], seg[1]):
            return False
    return True

# --- Example usage ---
if __name__ == "__main__":   

    office_coordinates, windows, desks, persons, disturbing_persons, moveable_walls = define_office_plan()
    
    # start_time = time.time()
    # for _ in range(1000):
    #     score = compute_office_score(windows, persons, disturbing_persons, moveable_walls)
    # end_time = time.time()
    # print(f"Elapsed time: {(end_time - start_time)/1000:.3f} seconds")

    score = compute_office_penalty(windows, persons, disturbing_persons, moveable_walls)
    print(f"Penalty Score: {score:.3f}")
