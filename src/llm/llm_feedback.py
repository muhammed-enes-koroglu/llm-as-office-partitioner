import pretty_errors
import path_helper
path_helper.add_project_path()
import json
import random

from office_score.check_collisions import detect_all_collisions
from office_score.penalty_score import compute_separate_penalties
import constants
import office_plans.office_plan as office_plan
from compare_penalties import compare_penalties

from llm.llm_visualization import visualize_llm_solution

Collision = tuple[tuple[float, float, float], int, tuple]
"""
Module: give_llm_feedback

Provides functionality to verify positions of movable walls in an office plan
and generate clear, modular feedback on any detected collisions.
"""

def describe_movable_wall_collision(movable_wall: tuple[float, float, float], info: tuple[float, float, float]) -> str:
    x, y, angle = movable_wall
    x2, y2, angle2 = info
    return f'- Movable wall ({x}, {y}, {angle}°) collides with another movable wall ({x2}, {y2}, {angle2}°).\n'


def describe_wall_collision(_: tuple[float, float, float], __: tuple) -> str:
    return '- Movable wall collides with a fixed office wall.\n'


def describe_desk_collision(_: tuple[float, float, float], info: tuple[float, float, float, float, float]) -> str:
    x, y, orientation, length, width = info
    half_l, half_w = length / 2, width / 2
    corners = [
        (x - half_l, y - half_w),
        (x + half_l, y - half_w),
        (x + half_l, y + half_w),
        (x - half_l, y + half_w),
    ]
    return f'- Movable wall collides with a desk: {json.dumps({"corners": corners})}.\n'


def describe_chair_collision(_: tuple[float, float, float], info: tuple[float, float, float]) -> str:
    x, y, radius = info
    return f'- Movable wall collides with a chair: {json.dumps({"center": (x, y), "radius": radius})}.\n'


def describe_door_collision(_: tuple[float, float, float], info: tuple[tuple[float, float], tuple[float, float], float, float]) -> str:
    hinge, end, angle, rotation = info
    door_data = {"hinge": hinge, "end": end, "open_angle_degrees": angle, "rotation": rotation}
    return f'- Movable wall collides with a door: {json.dumps(door_data)}.\n'


def describe_person_collision(_: tuple[float, float, float], info: tuple[float, float]) -> str:
    x, y = info
    return f'- Movable wall collides with a person at ({x}, {y}).\n'


def describe_object_collision(_: tuple[float, float, float], info: tuple[int, tuple]) -> str:
    obj_type, params = info
    if obj_type == constants.OBJECT_RECTANGLE:
        x, y, length, width = params
        data = {"type": obj_type, "center": (x, y), "length": length, "width": width}
    elif obj_type == constants.OBJECT_ROUND:
        x, y, radius = params
        data = {"type": obj_type, "center": (x, y), "radius": radius}
    elif obj_type == constants.OBJECT_POLYGON:
        data = {"type": obj_type, "corners": params}
    else:
        data = {"type": obj_type, "params": params}
    return f'- Movable wall collides with an object: {json.dumps(data)}.\n'
        

from typing import List, Tuple, Dict, Any

# Type aliases
WallConfig = Tuple[float, float, float]
MetricsList = List[Dict[str, Any]]

# Helper: Collision feedback

def _format_collision_feedback(collisions) -> str:
    if not collisions:
        return ''

    lines = [
        "⚠️ This is an invalid solution: a moveable wall intersects with office elements. Details:"
    ]
    describers = {
        constants.MOVABLE_WALL_COLLISION: describe_movable_wall_collision,
        constants.WALL_COLLISION: describe_wall_collision,
        constants.DESK_COLLISION: describe_desk_collision,
        constants.CHAIR_COLLISION: describe_chair_collision,
        constants.DOOR_COLLISION: describe_door_collision,
        constants.PERSON_COLLISION: describe_person_collision,
        constants.OBJECT_COLLISION: describe_object_collision,
    }
    for wall, ctype, info in collisions:
        func = describers.get(ctype)
        lines.append(func(wall, info) if func else f"- Unknown collision {ctype}: {info}")
    lines.append("Adjust your solution to prevent collisions.")
    return "\n".join(lines)

# Helper: Metrics feedback

def _format_metrics_feedback(metrics_list: MetricsList, header: str, number_of_windows: int, number_of_peers: int) -> str:
    lines = [header]
    FEEDBACK_ONLY = True
    for i, m in enumerate(metrics_list, 1):
        x, y, θ = m['wall']
        p = m['penalties_raw']
        pct = m['percentiles']
        if not FEEDBACK_ONLY:
            lines.append(f"Wall {i} (x={x:.2f}, y={y:.2f}, θ={θ}°):")
            lines.append(f" • Disturb: {p['disturb']:.2f} ({pct['disturb_pct']*100:.0f}%)")
            if number_of_windows > 0:
                lines.append(f" • Window : {p['window']:.2f} ({pct['window_pct']*100:.0f}%)")
            if number_of_peers > 0:
                lines.append(f" • Peers  : {p['vis']:.2f} ({pct['vis_pct']*100:.0f}%)")
        # suggestions
        sug = []
        if pct['disturb_pct'] > .7: sug.append("Disturbance caused by noise is too high!")
        elif pct['disturb_pct'] > .2: sug.append("Disturbance caused by noise is ok, but could be improved.")
        else: sug.append("Disturbance caused by noise is low, good!")

        if number_of_windows > 0:
            if pct['window_pct'] > .9: sug.append("Window exposure is low")
            elif pct['window_pct'] > .5: sug.append("Window exposure is ok, but could be improved.")
            else: sug.append("Window exposure is good!")

        if number_of_peers > 0:
            if pct['vis_pct'] > .9: sug.append("Visibility between workers is low")
            elif pct['vis_pct'] > .5: sug.append("Visibility between workers is ok, but could be improved.")
            else: sug.append("Visibility between workers is good!")

        lines.append(" → Suggestions:\n" + "\n".join(sug))
    return "\n".join(lines)

# Main function

def give_llm_feedback(iteration: int, moveable_walls: List[WallConfig]) -> str:
    # Load office plan
    office_coords, windows, doors, desks, persons, disturbing_persons, objects, disturbing_points, _ = \
        office_plan.define_office_plan()

    # 1) Check collisions
    collisions = detect_all_collisions(moveable_walls, office_coords, doors, desks, persons, objects)
    collision_msg = _format_collision_feedback(collisions)

    # 2) Compute penalties
    comparison_sample_size = 100
    metrics = compare_penalties(moveable_walls, comparison_sample_size)

    # 3) Build feedback
    feedback_parts = []
    if collision_msg:
        feedback_parts.append(collision_msg)
        header = ""
    else:
        header = f"✅ This is a valid solution, there are no collisions. \n"

    header += f"🔍 Additionally, I compared the solution with {comparison_sample_size} random layouts. This comparison examines noise reduction for every person, window exposure to every person and creating focused zones. This can give you information to improve:"

    number_of_windows = len(windows)
    number_of_peers = len(persons) - len(disturbing_persons)
    feedback_parts.append(_format_metrics_feedback(metrics, header, number_of_windows, number_of_peers))
    
    if constants.VISUALIZE_ONLY_VALID_SOLUTIONS:
        # visualize when no collisions
        if not collision_msg:
            visualize_llm_solution(iteration, moveable_walls)
    else: 
        visualize_llm_solution(iteration, moveable_walls)

    
    return "\n\n".join(feedback_parts) + "\n\n Use this information to propose a new solution. Explain again clearly why this solution satisfies all criteria.\n\n"

# --- Example usage ---
if __name__ == "__main__":
    
    # start_time = time.time()
    # for _ in range(1000):
    #     score = compute_office_score(windows, persons, disturbing_persons, moveable_walls)
    # end_time = time.time()
    # print(f"Elapsed time: {(end_time - start_time)/1000:.3f} seconds")

    moveable_walls = [(4.5,3.5,90)]
    feedback = give_llm_feedback(2, moveable_walls)
    print(feedback)