"""
Copyright (c) 2024 Friedrich Zimmer
Test in Town07 with several DRP patches as decals in various angles and mirrored positions
"""
from argparse import ArgumentParser

from util.camera_utils import RGBCamera
from util.test_class import CarlaTestRun

test_name = 't7_decal_DRP_all_cam'
town = 'Town07_attacked'
spawn_point = 84
x_cam = 1360
y_cam = 800
wait_between_tick = 0.3
fov = 120
ticks = 400
tick = 0.05
sensor_tick = 0.1

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
    test = CarlaTestRun([cam], name=test_name, spawn_point=spawn_point, ticks=ticks, folder=result_path, town=town)
    test.single_test_cycle('Default')
    test.end()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('r', type=str, help='Filepath and name of the results directory')
    args = parser.parse_args()
    main(args.r)
