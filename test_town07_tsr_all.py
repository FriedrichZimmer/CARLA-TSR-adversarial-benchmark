"""
Copyright (c) 2024 Friedrich Zimmer
Test of several traffic signs and adversarial examples in town07. This is done with several camera settings.
Attention! Running this script will need several hours and about 50 GB of disk space.
"""
from argparse import ArgumentParser

from util.camera_utils import RGBCamera
from util.test_class import CarlaTestRun
from util.update_texture import ROUND_TRAFFIC_SIGNS_TOWN7
from util.update_texture import TS_TEXTURE_CIRCLE

testname = 'T7_all_round_adv_cameras'
town = 'Town07_attacked'
spawn_point = 107
cycles = 498

# commented out as these are the default settings
# wait_between_tick = 0.3
# cycles_prep = 50
# tick = 0.05
# x_cam = 1360
# y_cam = 800

# List of textures for traffic signs. Each sign will be tested in a separate cycle
# full list can be imported or copied from util.update_texture
texture_list = TS_TEXTURE_CIRCLE

# when using a reduced list like this, the test will have only one repetition be much faster
# texture_list = [["Speed_40#Speed_60", "images\\textures_traffic_sign\\jia_40_60.png"]]


# list of cameras. Full list can be imported/copied from camera_utils.py
camera_tests = ['00_default_carla',
                '01_default_new',
                '10_mblur_low',
                '11_mblur_high',
                '30_iso_400',
                '31_iso_25',
                '40_high_gamma'
                ]

def main(folder):
    cam = RGBCamera(test_list=camera_tests)
    test = CarlaTestRun(cam, name=testname, spawn_point=spawn_point, ticks=cycles, folder=folder)
    test.run_texture(texture_list, ROUND_TRAFFIC_SIGNS_TOWN7)
    test.end()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("r", type=str, help="Filepath and name of the results directory")
    args = parser.parse_args()
    main(args.r)
