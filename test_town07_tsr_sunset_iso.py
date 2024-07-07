"""
Copyright (c) 2024 Friedrich Zimmer
Test of different brightness enhancers at bad lighting condition"""

from argparse import ArgumentParser
from util.camera_utils import RGBCamera
from util.test_class import CarlaTestRun
from util.update_texture import ROUND_TRAFFIC_SIGNS_TOWN7
from util.weather import *

town = 'Town07_attacked'
spawn_point = 107
cycles = 200

# commented out as these are the default settings
# sensor_tick = 0.1
# wait_between_tick = 0.3
# cycles_prep = 50
# tick = 0.05
# x_cam = 1360
# y_cam = 800

# list of cameras. Full list can be imported/copied from camera_utils.py
camera_tests = ['01_default_new',
                '20_low_shutter_speed',
                '30_iso_400',
                '40_high_gamma',
                '60_small_f_stop'
                ]

tsr_texture = [['Speed_30', 'images\\textures_traffic_sign\\tempo30_512.png']]


def main(result_path):
    cam = RGBCamera(test_list=camera_tests)

    test_name = "t7_tsr_sunset_all"
    test = CarlaTestRun(cam, name=test_name, spawn_point=spawn_point, ticks=cycles, folder=result_path, town=town)
    test.set_weather(sunset(0, 1.0))
    test.run_texture(tsr_texture, ROUND_TRAFFIC_SIGNS_TOWN7)

    test.end()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("r", type=str, help="Filepath and name of the results directory")
    args = parser.parse_args()
    main(args.r)
