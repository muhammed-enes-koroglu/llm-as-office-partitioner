import path_helper
path_helper.add_project_path()

import pretty_errors
import math
import constants
import utils.utils_desk as utils_desk
import importlib
from office_plans.office_plan import define_office_plan
import time

importlib.reload(utils_desk)
importlib.reload(pretty_errors)

# --------------------------
# Helper: Compute rotated rectangle vertices
# --------------------------
def get_rectangle_polygon(x, y, length, width, angle):
    """
    Returns the 4 vertices of a rectangle after rotation about its center.
    
    Parameters:
      x, y       : Reference coordinate (middle of the rectangle)
      length     : Length (x-direction)
      width      : Width (y-direction)
      angle      : Rotation angle in degrees (clockwise or counterclockwise as desired)
      
    Returns:
      A list of four (x, y) tuples representing the rotated rectangle.
    """
    # Define rectangle corners at angle==0 (axis-aligned)
    # For origin 'lower_left', the corners are:
    ll = (x - length/2, y - width/2)
    lr = (x + length/2, y - width/2)
    ur = (x + length/2, y + width/2)
    ul = (x - length/2, y + width/2)
    
    # Pre-calculate sine and cosine of the angle (converted to radians)
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    rotated = []
    for px, py in [ll, lr, ur, ul]:
        # Translate the point relative to the center
        dx = px - x
        dy = py - y
        # Rotate the point
        rx = dx * cos_a - dy * sin_a
        ry = dx * sin_a + dy * cos_a
        # Translate back
        rotated.append((x + rx, y + ry))
    return rotated

# --------------------------
# Helper: Check collision between two convex polygons using the Separating Axis Theorem (SAT)
# --------------------------
def polygons_intersect(poly1, poly2):
    """
    Uses the Separating Axis Theorem (SAT) to determine whether two convex polygons intersect.
    Reference: https://www.metanetsoftware.com/technique/tutorialA.html
    """
    def get_axes(poly):
        axes = []
        n = len(poly)
        for i in range(n):
            p1 = poly[i]
            p2 = poly[(i + 1) % n]
            # Edge vector
            edge = (p2[0] - p1[0], p2[1] - p1[1])
            # The perpendicular (normal) axis
            normal = (-edge[1], edge[0])
            # Normalize the axis
            length = math.hypot(normal[0], normal[1])
            if length != 0:
                normal = (normal[0] / length, normal[1] / length)
            axes.append(normal)
        return axes

    def project(poly, axis):
        min_val = float('inf')
        max_val = -float('inf')
        for p in poly:
            proj = p[0] * axis[0] + p[1] * axis[1]
            min_val = min(min_val, proj)
            max_val = max(max_val, proj)
        return min_val, max_val

    # Get the projection axes from both polygons
    axes = get_axes(poly1) + get_axes(poly2)
    for axis in axes:
        min1, max1 = project(poly1, axis)
        min2, max2 = project(poly2, axis)
        # If there is a gap on this axis, then no collision
        if max1 < min2 or max2 < min1:
            return False
    return True

# --------------------------
# Helper: Check if a point is inside a polygon (ray-casting method)
# --------------------------
def point_in_polygon(point, poly):
    x, y = point
    inside = False
    n = len(poly)
    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]
        if ((p1y > y) != (p2y > y)) and \
           (x < (p2x - p1x) * (y - p1y) / (p2y - p1y + 1e-9) + p1x):
            inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# --------------------------
# Helper: Check if two line segments intersect
# --------------------------
def segments_intersect(p, q, r, s):
    def orientation(a, b, c):
        val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
        if abs(val) < 1e-9:
            return 0  # collinear
        return 1 if val > 0 else 2  # 1: clockwise, 2: counterclockwise

    def on_segment(a, b, c):
        return (min(a[0], c[0]) <= b[0] <= max(a[0], c[0]) and
                min(a[1], c[1]) <= b[1] <= max(a[1], c[1]))

    o1 = orientation(p, q, r)
    o2 = orientation(p, q, s)
    o3 = orientation(r, s, p)
    o4 = orientation(r, s, q)

    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(p, r, q):
        return True
    if o2 == 0 and on_segment(p, s, q):
        return True
    if o3 == 0 and on_segment(r, p, s):
        return True
    if o4 == 0 and on_segment(r, q, s):
        return True
    return False

# --------------------------
# Helper: Check if a line segment intersects a polygon
# --------------------------
def line_intersects_polygon(p, q, poly):
    n = len(poly)
    for i in range(n):
        a = poly[i]
        b = poly[(i + 1) % n]
        if segments_intersect(p, q, a, b):
            return True
    return False

def distance_point_to_segment(p, a, b):
    """Return the minimum distance from point p to the line segment ab."""
    # p, a, b are (x, y) tuples
    # Compute the vector from a to p and from a to b.
    ap = (p[0] - a[0], p[1] - a[1])
    ab = (b[0] - a[0], b[1] - a[1])
    ab_len2 = ab[0]**2 + ab[1]**2
    if ab_len2 == 0:
        return math.hypot(ap[0], ap[1])
    # Project p onto ab, computing parameterized position t
    t = (ap[0]*ab[0] + ap[1]*ab[1]) / ab_len2
    t = max(0, min(1, t))  # Clamp t to the segment
    projection = (a[0] + t * ab[0], a[1] + t * ab[1])
    return math.hypot(p[0] - projection[0], p[1] - projection[1])

def circle_intersects_polygon(center, radius, poly):
    """
    Checks whether a circle (center, radius) intersects a polygon.
    Returns True if the circle's center is inside the polygon or if the circle
    intersects any polygon edge.
    """
    # If center is inside the polygon, there's a collision.
    if point_in_polygon(center, poly):
        return True
    # Otherwise, check each edge for proximity.
    n = len(poly)
    for i in range(n):
        a = poly[i]
        b = poly[(i+1) % n]
        if distance_point_to_segment(center, a, b) <= radius:
            return True
    return False

def arc_intersects_polygon(center, arc_startpoint, angle, rotation, poly, segments=30):
    """
    Checks if an arc (part of circle) intersects a polygon.
    - `center`: (x, y) centre of the circle.
    - `arc_startpoint`: (x, y) start of the arc.
    - `angle`: degrees of arc (e.g. 90° means quarter circle).
    - `rotation`: constants.CLOCKWISE or constants.COUNTERCLOCKWISE.
    - `poly`: array of (x, y).
    - `segments`: generated points on arc.
    """
    cx, cy = center
    px, py = arc_startpoint
    radius = math.hypot(px - cx, py - cy)

    if rotation == constants.CLOCKWISE:
        rotation_p = -1
    else: rotation_p = 1
    
    # Calculate start angle
    start_angle = math.atan2(py - cy, px - cx)

    # Generate points on arc
    arc_points = []
    for i in range(segments + 1):
        theta = start_angle + rotation_p * math.radians(angle) * (i / segments)
        arc_x = cx + radius * math.cos(theta)
        arc_y = cy + radius * math.sin(theta)
        arc_points.append((arc_x, arc_y))

    poly_arc = arc_points + [center]
    return polygons_intersect(poly_arc, poly)




# --------------------------
# Main Collision Check Function
# --------------------------
def check_collision(moveable_wall, other_object, object_type):
    """
    Checks if a given moveable wall collides with another object.
    
    Parameters:
      movable_wall: tuple (x, y, angle)
        - (x, y) is the middle of the moveable wall as defined in draw_movable_wall.py.
        - angle is in degrees.
      other_object: tuple with parameters that depend on the type:
        - For "movable_wall": (x, y, angle)
        - For "desk": (x, y, orientation, length, width)
        - For "wall": (x1, y1, x2, y2) defining a line segment.
        - For "window": (x, y, size, orientation) where the endpoints are computed using utils_window.get_window_coordinates_2d.
        - For "person": (x, y)
      object_type: string indicating the type ("movable_wall", "desk", "wall", "window", "person").
      
    Returns:
      True if a collision is detected, False otherwise.
    """
    # Get the polygon for the moveable wall using its standard dimensions
    mw_poly = get_rectangle_polygon(
        moveable_wall[0], moveable_wall[1],
        constants.MOVABLE_WALL_LENGTH, constants.MOVABLE_WALL_WIDTH,
        moveable_wall[2]
    )
    
    if object_type == constants.MOVABLE_WALL_COLLISION:
        # Other moveable wall (same dimensions and rotation)
        other_poly = get_rectangle_polygon(
            other_object[0], other_object[1],
            constants.MOVABLE_WALL_LENGTH, constants.MOVABLE_WALL_WIDTH,
            other_object[2]
        )
        return polygons_intersect(mw_poly, other_poly)
    
    elif object_type == constants.DESK_COLLISION:
        # Desk: defined as (x, y, orientation) but the desk itself is drawn as an axis-aligned rectangle.
        # We assume the desk rectangle has its middle at (x,y)
        x, y, orientation, desk_length, desk_width = other_object
        desk_poly = [
            (x - desk_length/2, y - desk_width/2),
            (x + desk_length/2, y - desk_width/2),
            (x + desk_length/2, y + desk_width/2),
            (x - desk_length/2, y + desk_width/2)
        ]
        return polygons_intersect(mw_poly, desk_poly)
    
    elif object_type == constants.DOOR_COLLISION:
        # Door: defined as (hinge, door_end, opening_angle, rotation)
        hinge, door_end, opening_angle, rotation = other_object
        return arc_intersects_polygon(hinge, door_end, opening_angle, rotation, mw_poly)
    
    # elif object_type == "wall":
    #     # Wall: defined as a line segment (x1, y1, x2, y2)
    #     p1 = (other_object[0], other_object[1])
    #     p2 = (other_object[2], other_object[3])
    #     # Check if either endpoint is inside the moveable wall or if the segment intersects any edge
    #     if point_in_polygon(p1, mw_poly) or point_in_polygon(p2, mw_poly):
    #         return True
    #     if line_intersects_polygon(p1, p2, mw_poly):
    #         return True
    #     return False
    
    elif object_type == constants.WALL_COLLISION:
        # Window: defined as (x, y, size, orientation)
        # Import the helper from utils_window to compute its endpoints in 2D (ignoring z)
        office_coordinates = []
        if other_object[0] == constants.OFFICE_RECTANGLE:
            office_length, office_width = other_object[1]
            office_coordinates = [(0,0), (office_length, 0), (office_length, office_width), (0, office_width)]
        if other_object[0] == constants.OFFICE_POLYGON:
            office_coordinates = other_object[1]
        for mw_point in mw_poly:
            if not point_in_polygon(mw_point, office_coordinates):
                return True
            
    elif object_type == constants.PERSON_COLLISION:
        # Person: defined as a point (x, y)
        # Here we check if the person is located inside the moveable wall.
        # (Depending on requirements you might also wish to enforce a clearance distance.)
        return point_in_polygon(other_object, mw_poly)
    
    elif object_type == constants.CHAIR_COLLISION:
        # Assuming other_object is a tuple: (center_x, center_y, radius)
        center = (other_object[0], other_object[1])
        radius = other_object[2]
        return circle_intersects_polygon(center, radius, mw_poly)
    
    elif object_type == constants.OBJECT_COLLISION:
        # Assuming other_object as: [object_type, object_info]
        if other_object[0] == constants.OBJECT_POLYGON:
            return polygons_intersect(mw_poly, other_object[1])
        if other_object[0] == constants.OBJECT_RECTANGLE:
            x, y, length, width = other_object[1]
            angle = 0
            other_poly = get_rectangle_polygon(
                x, y,length, width, angle
            )
            return polygons_intersect(mw_poly, other_poly)
        if other_object[0] == constants.OBJECT_ROUND:
            x, y, radius = other_object[1]
            center = (x,y)
            return circle_intersects_polygon(center, radius, mw_poly)
    
    else:
        raise ValueError("Unsupported object_type for collision detection.")


def detect_all_collisions(moveable_walls, office_coordinates, doors, desks, persons, objects):
    """
    Detect collisions between all moveable walls and other objects:
    doors, desks, persons, objects and moveable walls.
    
    Each moveable wall is defined as (x, y, angle).
    - doors: ((x, y), (x,y), opening_angle, rotation)
    - desks: (x, y, orientation)
    - persons: (x, y)
    - objects: (object_type, object_info)
    
    Chairs are computed from desks via utils_desk.get_chair_coordinate and are represented 
    as a circle with center (x, y) and radius constants.CHAIR_RADIUS.
    
    Returns:
        A list of collisions. Each collision is represented as a tuple:
        (movable_wall, other_object, object_type)
    """
    collisions = []
    
    # Loop over each moveable wall
    for i, mw in enumerate(moveable_walls):
        # Check collision with office walls
        if check_collision(mw, office_coordinates, constants.WALL_COLLISION):
            collisions.append((mw, constants.WALL_COLLISION, office_coordinates))
        
        # Check collision with desks
        for desk in desks:
            if check_collision(mw, desk, constants.DESK_COLLISION):
                collisions.append((mw, constants.DESK_COLLISION, desk))
        
        # Check collision with chairs (derived from desks)
        for desk in desks:
            chair_center = utils_desk.get_chair_coordinate(desk)
            chair = (chair_center[0], chair_center[1], constants.CHAIR_RADIUS)
            if check_collision(mw, chair, constants.CHAIR_COLLISION):
                collisions.append((mw, constants.CHAIR_COLLISION, chair))

        # Check collision with doors
        for door in doors:
            if check_collision(mw, door, constants.DOOR_COLLISION):
                collisions.append((mw, constants.DOOR_COLLISION, door))

        # Check collision with persons
        for person in persons:
            if check_collision(mw, person, constants.PERSON_COLLISION):
                collisions.append((mw, constants.PERSON_COLLISION, person))

        for object in objects:
            if check_collision(mw, object, constants.OBJECT_COLLISION):
                collisions.append((mw, constants.OBJECT_COLLISION, object))
        
        # Check collision with other moveable walls (avoid duplicate checks)
        for j, other_mw in enumerate(moveable_walls):
            if j > i:
                if check_collision(mw, other_mw, constants.MOVABLE_WALL_COLLISION):
                    collisions.append((mw, constants.MOVABLE_WALL_COLLISION, other_mw))
                    
    return collisions



# --------------------------
# Example usage:
# --------------------------
if __name__ == "__main__":
    # Define a moveable wall at (3, 2) with a rotation of 90 degrees.
    # mw = (3, 2, 90)
    
    # Example: Check collision with a desk at (1, 2.5) (orientation is not used for the desk shape)
    # desk = (1, 2.5, constants.ORIENTATION_DOWN)
    # collision_with_desk = check_collision(mw, desk, "desk")
    # print("Collision with desk:", collision_with_desk)
    
    # # Example: Check collision with a wall (line segment from (0,0) to (8,0))
    # wall = (0, 0, 8, 0)
    # collision_with_wall = check_collision(mw, wall, "wall")
    # print("Collision with wall:", collision_with_wall)
    
    # # Example: Check collision with a person at (4, 3)
    # person = (4, 3)
    # collision_with_person = check_collision(mw, person, "person")
    # print("Collision with person:", collision_with_person)
    
    start_time = time.time()
    for _ in range(100):
        office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, disturbing_points, moveable_walls = define_office_plan()
        collisions_found = detect_all_collisions(moveable_walls, office_coordinates, doors, desks, persons, objects)
    print("Time taken:", (time.time() - start_time)/1000)
    print("Collisions found:", collisions_found)
    
