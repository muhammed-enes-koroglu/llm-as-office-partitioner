import pretty_errors
import statistics
from typing import List, Tuple, Dict, Any
import random
import path_helper
path_helper.add_project_path()

from office_score.check_collisions import detect_all_collisions
from office_score.penalty_score import compute_separate_penalties
import office_plans.office_plan as office_plan
import constants
# Type aliases
WallConfig     = Tuple[float, float, float]         # (x, y, θ)
PenaltyTriple  = Tuple[float, float, float]         # (P_disturb, P_window, P_vis)
StatsDict      = Dict[str, Dict[str, float]]        # e.g. {"disturb": {"mean": ..., "std": ..., ...}, ...}
MetricsDict    = Dict[str, Any]                     # final per‐wall report

def generate_random_configurations(num_configs, office_coords, doors, desks, persons, objects) -> list[tuple[float, float, float]]:
    """
    Generate random valid configurations for movable walls in the office space.

    Args:
        num_configs (int): Number of random configurations to generate.
        office_coords (tuple[Literal['RECTANGLE'], tuple[int, int]] | tuple[Literal['POLYGON'], list[tuple[int, int]]]).
        doors (Any): List of door objects or coordinates.
        desks (Any): List of desk objects or coordinates.
        persons (Any): List of person objects or coordinates.
        objects (Any): List of other objects in the office.

    Returns:
        List[Tuple[float, float, float]]: List of valid wall configurations as (x, y, theta).
    """
    configurations = []

    # Get office bounding box
    right_most = 0
    top_most = 0
    if office_coords[0] == constants.OFFICE_RECTANGLE:
        office_length, office_width = office_coords[1]
        right_most = office_length # highest x
        top_most = office_width # highest y
    
    if office_coords[0] == constants.OFFICE_POLYGON:
        right_most = max(office_coords[1], key=lambda p: p[0])[0] # highest x
        top_most = max(office_coords[1], key=lambda p: p[1])[1] # highest y


    while len(configurations) < num_configs:
        x = random.uniform(0, right_most)
        y = random.uniform(0, top_most)
        theta = random.uniform(-90, 90)

        # Create a candidate configuration
        candidate = (x, y, theta)

        # Check for collisions
        collisions = detect_all_collisions([candidate], office_coords, doors, desks, persons, objects)
        if not collisions:
            configurations.append(candidate)
    return configurations

def compute_baseline_stats(penalties: List[PenaltyTriple]) -> StatsDict:
    """Compute mean, std, min, max for each of the three penalty dimensions."""
    pd_list, pw_list, pv_list = zip(*penalties)
    return {
        "disturb": { "mean": statistics.mean(pd_list),
                     "std":  statistics.pstdev(pd_list),
                     "min":  min(pd_list),
                     "max":  max(pd_list) },
        "window":  { "mean": statistics.mean(pw_list),
                     "std":  statistics.pstdev(pw_list),
                     "min":  min(pw_list),
                     "max":  max(pw_list) },
        "vis":     { "mean": statistics.mean(pv_list),
                     "std":  statistics.pstdev(pv_list),
                     "min":  min(pv_list),
                     "max":  max(pv_list) }
    }

def z_score(value: float, mean: float, std: float) -> float:
    """Standard score; zero if std==0."""
    return (value - mean) / std if std else 0.0

def min_max_norm(value: float, vmin: float, vmax: float) -> float:
    """Scale into [0,1]; zero if all values identical."""
    return (value - vmin) / (vmax - vmin) if vmax != vmin else 0.0

def compute_percentile(value: float, data: List[float]) -> float:
    """Fraction of data points ≤ value."""
    return sum(1 for v in data if v <= value) / len(data)

def compare_penalties(moveable_walls: List[WallConfig], comparison_sample_size: int = 100) -> List[MetricsDict]:
    # Load static office elements
    office_coords, windows, doors, desks, persons, disturbing_persons, objects, disturbing_points, _ = \
        office_plan.define_office_plan()

    # 1) Generate one big common baseline set
    total_samples = comparison_sample_size * len(moveable_walls)
    common_baseline_confs = generate_random_configurations(
        total_samples, office_coords, doors, desks, persons, objects
    )

    # 2) Compute baseline penalties once (same for every wall)
    #    pd_list: list of disturbance penalties for each random conf
    #    pw_list: list of window obstruction penalties for each random conf
    #    pv_list: list of visibility reduction penalties for each random conf
    baseline_penalties = [
        compute_separate_penalties(windows, persons, disturbing_persons+disturbing_points, [conf])
        for conf in common_baseline_confs
    ]
    stats = compute_baseline_stats(baseline_penalties)
    pd_list, pw_list, pv_list = zip(*baseline_penalties)

    all_results: List[MetricsDict] = []

    for wall in moveable_walls:
        # 3) Compute penalties for this suggested wall
        #    pd_s: disturbance penalty for this wall
        #    pw_s: window obstruction penalty for this wall
        #    pv_s: visibility reduction penalty for this wall
        pd_s, pw_s, pv_s = compute_separate_penalties(
            windows, persons, disturbing_persons+disturbing_points, [wall]
        )

        # 4) Normalize & percentile
        normalized = {
            "disturb_z":  z_score(pd_s, stats["disturb"]["mean"], stats["disturb"]["std"]),
            "window_z":   z_score(pw_s, stats["window"]["mean"],  stats["window"]["std"]),
            "vis_z":      z_score(pv_s, stats["vis"]["mean"],     stats["vis"]["std"]),

            "disturb_mm": min_max_norm(pd_s, stats["disturb"]["min"], stats["disturb"]["max"]),
            "window_mm":  min_max_norm(pw_s, stats["window"]["min"],  stats["window"]["max"]),
            "vis_mm":     min_max_norm(pv_s, stats["vis"]["min"],     stats["vis"]["max"]),
        }

        percentiles = {
            "disturb_pct": compute_percentile(pd_s, pd_list),
            "window_pct":  compute_percentile(pw_s, pw_list),
            "vis_pct":     compute_percentile(pv_s, pv_list) if len(persons) - len(disturbing_persons) > 1 else 0,
        }
        # 5) Collect results
        all_results.append({
            "wall":            wall,
            "penalties_raw":   { "disturb": pd_s, "window": pw_s, "vis": pv_s },
            "stats_baseline":  stats,
            "normalized":      normalized,
            "percentiles":     percentiles
        })

    return all_results
