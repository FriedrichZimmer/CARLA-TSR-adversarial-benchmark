"""
Copyright (c) 2024 Friedrich Zimmer
Test for the dirty road patch attack in town 07 with the patch as street texture
"""


from argparse import ArgumentParser

from util.camera_utils import RGBCamera
from util.test_class import CarlaTestRun

# from util.update_texture import TS_TEXTURE_CIRCLE
# import util.weather

test_name = 't7_drp_camera'
town = 'Town07_attacked'
spawn_point = 48
cycles = 220
cycles_prep = 80
# commented out as these are the default settings of the camera
sensor_tick = 0.1
# wait_between_tick = 0.25
# tick = 0.05
# x_cam = 1360
# y_cam = 800

# list of cameras. Full list can be imported/copied from camera_utils.py
camera_tests = ['00_default_carla',
                '01_default_new',
                '10_mblur_low',
                '11_mblur_high',
                '30_iso_400',
                '31_iso_25',
                '40_high_gamma'
                ]


def main(result_path):
    cam = RGBCamera(test_list=camera_tests)
    test = CarlaTestRun(cam, name=test_name, spawn_point=spawn_point, ticks=cycles, folder=result_path, town=town)
    test.single_test_cycle('Default')
    test.end()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("r", type=str, help="Filepath and name of the results directory")
    args = parser.parse_args()
    main(args.r)
