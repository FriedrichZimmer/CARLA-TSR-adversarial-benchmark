"""
Copyright (c) 2024 Friedrich Zimmer
test with different weather conditions for the recognition of the speed 30 sign
custom actors have to be added beforehand"""

from argparse import ArgumentParser
from util.camera_utils import RGBCamera
from util.test_class import CarlaTestRun
from util.update_texture import ROUND_TRAFFIC_SIGNS_TOWN7
from util.weather import *

town = 'Town07_attacked'
spawn_point = 107
cycles = 498

# commented out as these are the default settings
# sensor_tick = 0.1
# wait_between_tick = 0.3
# cycles_prep = 50
# tick = 0.05
# x_cam = 1360
# y_cam = 800

# list of cameras. Full list can be imported/copied from camera_utils.py
camera_tests = ["01_default_new"]

# list of textures of traffic signs. Each sign will result in another testrun.
# Full list can be imported from update_texture.py
tsr_texture = [['Speed_30', 'images\\textures_traffic_sign\\Eg_Hvb.png']]

def main(result_path):
    """testscript for weather test"""
    cam = RGBCamera(test_list=camera_tests)

    test_name = "t7_tsr_sunset_all"
    test = CarlaTestRun(cam, name=test_name, spawn_point=spawn_point, ticks=cycles, folder=result_path, town=town)
    test.set_weather(sunset(0))
    test.run_texture(tsr_texture, ROUND_TRAFFIC_SIGNS_TOWN7)

    # test_name = "t7_tsr_foggy_all"
    # test = CarlaTestRun(cam, name=test_name, spawn_point=spawn_point, ticks=cycles, folder=result_path, town=town)
    # test.set_weather(foggy())
    # test.run_texture(tsr_texture, ROUND_TRAFFIC_SIGNS_TOWN7)

    # test_name = "t7_tsr_heavy_rain"
    # test = CarlaTestRun(cam, name=test_name, spawn_point=spawn_point, ticks=cycles, folder=result_path, town=town)
    # test.set_weather(heavy_rain())
    # test.run_texture(TS_TEXTURE_CIRCLE, ROUND_TRAFFIC_SIGNS_TOWN7)

    test.end()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("r", type=str, help="Filepath and name of the results directory")
    args = parser.parse_args()
    main(args.r)
