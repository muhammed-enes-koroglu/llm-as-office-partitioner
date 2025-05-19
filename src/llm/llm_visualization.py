import path_helper
path_helper.add_project_path()

import os
import matplotlib.pyplot as plt

import office_plans.office_plan as office_plan
from draw_python.draw import draw_office_plan
from draw_python.make_image import create_image

import constants

def visualize_llm_solution(iteration, moveable_walls):

    if constants.LLM_VISUALIZATION == constants.VISUALIZE_AS_MULTIPLE_IMAGES:
        visualize_llm_solution_multiple_images(iteration, moveable_walls)

    if constants.LLM_VISUALIZATION == constants.VISUALIZE_AS_ONE_IMAGE:
        visualize_llm_solution_one_image(iteration, moveable_walls)


def visualize_llm_solution_multiple_images(iteration, moveable_walls):
        
        office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, noise, _ = office_plan.define_office_plan()
        
        # Create figure and draw office
        fig, ax = plt.subplots()
        draw_office_plan(ax, office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, noise, moveable_walls, iteration)

        # Make sure folder exists and create image
        os.makedirs(constants.FOLDERNAME, exist_ok=True)
        
        if iteration == -1:
            filename = constants.FOLDERNAME + '/office_plan' + str(constants.CURRENT_OFFICE_PLAN) + '_final.png'
        else: filename = constants.FOLDERNAME + '/office_plan' + str(constants.CURRENT_OFFICE_PLAN) + '_iteration' + str(iteration) + '.png'
        create_image(ax, filename, office_coordinates)


def visualize_llm_solution_one_image(iteration, moveable_walls):
        office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, noise, _ = office_plan.define_office_plan()

        if iteration == -1:
            # Make sure folder exists and create image
            os.makedirs(constants.FOLDERNAME, exist_ok=True)
            filename = constants.FOLDERNAME + '/office_plan' + str(constants.CURRENT_OFFICE_PLAN) + '.png'
            create_image(ax_one_image, filename, office_coordinates)

        else: draw_office_plan(ax_one_image, office_coordinates, windows, doors, desks, persons, disturbing_persons, objects, noise, moveable_walls, iteration)




fig_one_image, ax_one_image = plt.subplots()