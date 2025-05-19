import path_helper
path_helper.add_project_path()

import office_plans.office_plan as office_plan
import create_prompt
import constants


office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, disturbing_points, moveable_walls = office_plan.define_office_plan()

print(create_prompt.create_prompt(office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, disturbing_points,prompt_type=constants.CURRENT_PROMPT_TYPE))
