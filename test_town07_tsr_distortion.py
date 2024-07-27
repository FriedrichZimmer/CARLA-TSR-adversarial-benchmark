"""
Copyright (c) 2024 Friedrich Zimmer
test with different weather conditions for the recognition of the speed 30 sign
custom actors have to be added beforehand"""

from argparse import ArgumentParser
from util.camera_utils import RGBCamera
from util.test_class import CarlaTestRun
from util.update_texture import ROUND_TRAFFIC_SIGNS_TOWN7
from util.weather import *

test_name = "t7_distortion_test"
town = 'Town07_attacked'
spawn_point = 107
cycles = 1

# commented out as these are the default settings
# sensor_tick = 0.1
# wait_between_tick = 0.3
# cycles_prep = 50
# tick = 0.05
# x_cam = 1360
# y_cam = 800

# list of cameras. Full list can be imported/copied from camera_utils.py
camera_tests = ['80_lens_circle_multiplier_1',
                '81_lens_circle_multiplier_2',
                '72_lens_circle_multiplier_5',
                '82_lens_circle_multiplier_10'
                ]

# list of textures of traffic signs. Each sign will result in another testrun.
# Full list can be imported from update_texture.py
tsr_texture = [['Speed_30', 'images\\textures_traffic_sign\\Eg_Hvb.png']]

def main(result_path):
    cam = RGBCamera(test_list=camera_tests)

    test = CarlaTestRun([cam], name=test_name, spawn_point=spawn_point, ticks=cycles, folder=result_path, town=town)
    test.run_texture(tsr_texture, ROUND_TRAFFIC_SIGNS_TOWN7)
    test.end()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("r", type=str, help="Filepath and name of the results directory")
    args = parser.parse_args()
    main(args.r)
