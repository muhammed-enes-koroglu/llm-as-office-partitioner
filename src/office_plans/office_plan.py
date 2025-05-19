import path_helper
path_helper.add_project_path()

import constants
import importlib
import office_plans.office_plan_example1 as office_plan0
import office_plans.office_plan1 as office_plan1
import office_plans.office_plan2 as office_plan2
import office_plans.office_plan3 as office_plan3
import office_plans.office_plan4 as office_plan4
import office_plans.office_plan5 as office_plan5
import office_plans.office_plan6 as office_plan6
import office_plans.office_plan7 as office_plan7
import office_plans.office_plan8 as office_plan8
import office_plans.office_plan9 as office_plan9
import office_plans.office_plan10 as office_plan10
import office_plans.office_plan11 as office_plan11
import office_plans.office_plan12 as office_plan12
import office_plans.office_plan13 as office_plan13
import office_plans.office_plan14 as office_plan14
import office_plans.office_plan15 as office_plan15
import office_plans.office_plan16 as office_plan16
import office_plans.office_plan17 as office_plan17
import office_plans.office_plan18 as office_plan18
import office_plans.office_plan19 as office_plan19
import office_plans.office_plan20 as office_plan20
import office_plans.office_plan21 as office_plan21
import office_plans.office_plan22 as office_plan22

importlib.reload(constants)
importlib.reload(office_plan0)
importlib.reload(office_plan1)
importlib.reload(office_plan2)
importlib.reload(office_plan3)
importlib.reload(office_plan4)
importlib.reload(office_plan5)
importlib.reload(office_plan6)
importlib.reload(office_plan7)
importlib.reload(office_plan8)
importlib.reload(office_plan9)
importlib.reload(office_plan10)
importlib.reload(office_plan11)
importlib.reload(office_plan12)
importlib.reload(office_plan13)
importlib.reload(office_plan14)
importlib.reload(office_plan15)
importlib.reload(office_plan16)
importlib.reload(office_plan17)
importlib.reload(office_plan18)
importlib.reload(office_plan19)
importlib.reload(office_plan20)
importlib.reload(office_plan21)
importlib.reload(office_plan22)


def define_office_plan(current_office_plan=constants.CURRENT_OFFICE_PLAN):

    if current_office_plan == 0:
        return office_plan0.define_office_plan()

    if current_office_plan == 1:
        return office_plan1.define_office_plan()
    if current_office_plan == 2:
        return office_plan2.define_office_plan()
    if current_office_plan == 3:
        return office_plan3.define_office_plan()
    if current_office_plan == 4:
        return office_plan4.define_office_plan()
    if current_office_plan == 5:
        return office_plan5.define_office_plan()
    if current_office_plan == 6:
        return office_plan6.define_office_plan()
    if current_office_plan == 7:
        return office_plan7.define_office_plan()
    if current_office_plan == 8:
        return office_plan8.define_office_plan()
    if current_office_plan == 9:
        return office_plan9.define_office_plan()
    if current_office_plan == 10:
        return office_plan10.define_office_plan()
    if current_office_plan == 11:
        return office_plan11.define_office_plan()
    if current_office_plan == 12:
        return office_plan12.define_office_plan()
    if current_office_plan == 13:
        return office_plan13.define_office_plan()
    if current_office_plan == 14:
        return office_plan14.define_office_plan()
    if current_office_plan == 15:
        return office_plan15.define_office_plan()
    if current_office_plan == 16:
        return office_plan16.define_office_plan()
    if current_office_plan == 17:
        return office_plan17.define_office_plan()
    if current_office_plan == 18:
        return office_plan18.define_office_plan()
    if current_office_plan == 19:
        return office_plan19.define_office_plan()
    if current_office_plan == 20:
        return office_plan20.define_office_plan()
    if current_office_plan == 21:
        return office_plan21.define_office_plan()
    if current_office_plan == 22:
        return office_plan22.define_office_plan()
    