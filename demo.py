"""
Copyright (c) 2024 Friedrich Zimmer
A demo that shows all important settings"""

from util.camera_utils import RGBCamera
from util.test_class import CarlaTestRun
from util.update_texture import ROUND_TRAFFIC_SIGNS_TOWN7
from util.weather import *

# Test settings:
# some are commented out as these are the default settings
test_name = 't7_tsr_sunset'
result_path = 'C:/temp/Results'
spawn_point = 107
# ticks_prep = 50
ticks = 498
# tick_length = 0.05
town = 'Town07_attacked'

# Camera Settings:
# x_cam = 1360
# y_cam = 800
# fov = 120
# tick = 0.1
# list of cameras. Full list can be imported/copied from camera_utils.py
camera_tests = ['01_default_new',
                '30_iso_400']
# campos = carla.Location(x=0.6, z=1.45
# save_time = 0.25
cam = RGBCamera(test_list=camera_tests)

test = CarlaTestRun([cam], name=test_name, spawn_point=spawn_point, ticks=ticks, folder=result_path, town=town)
# Set the Weather
test.set_weather(sunset(0))

# list of textures of traffic signs. Each sign will result in another testrun.
# Full list can be imported from update_texture.py
tsr_texture = [['Speed_50', 'images\\textures_traffic_sign\\tempo50_512.png'],
               ['Speed_50#Speed_30', 'images\\textures_traffic_sign\\morg_50_30.png']]
test.run_texture(tsr_texture, ROUND_TRAFFIC_SIGNS_TOWN7)

test.end()
