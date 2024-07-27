"""
Copyright (c) 2024 Friedrich Zimmer
Example on how cameras with different resolutions at different positions can be set up.
Running this test will need about 15-20 minutes.
"""
from argparse import ArgumentParser
import carla

from util.camera_utils import RGBCamera
from util.test_class import CarlaTestRun
from util.update_texture import ROUND_TRAFFIC_SIGNS_TOWN7

testname = 'T7_five_cameras'
town = 'Town07_attacked'
spawn_point = 107
cycles = 498

# when using a reduced list like this, the test will have only one repetition be much faster.
# This list contains only a single traffic sign
tsr_texture = [['Speed_30', 'images\\textures_traffic_sign\\tempo30_512.png']]


def main(folder):
    camera_tests = ['02_auto_exposure']
    cameras = []
    campos = carla.Transform(carla.Location(x=0.6, z=1.45))
    cam_highres = RGBCamera(cam_name="Front_HR", x_cam=2400, y_cam=1600, test_list=camera_tests,
                            campos=campos, save_time=2.0)
    cameras.append(cam_highres)
    campos = carla.Transform(carla.Location(x=2.35, z=0.4), carla.Rotation(pitch=-20.0))
    cam_front = RGBCamera(cam_name="Front", x_cam=1536, y_cam=1024, test_list=camera_tests,
                          campos=campos, save_time=2.0)
    cameras.append(cam_front)
    campos = carla.Transform(carla.Location(x=-2.3, z=0.4), carla.Rotation(yaw=180.0, pitch=-20.0))
    cam_rear = RGBCamera(cam_name="Rear", x_cam=1536, y_cam=1024, test_list=camera_tests,
                         campos=campos, save_time=2.0)
    cameras.append(cam_rear)
    campos = carla.Transform(carla.Location(x=0.55, y=1.1, z=1.1), carla.Rotation(yaw=90.0, pitch=-20.0))
    cam_right = RGBCamera(cam_name="Right", x_cam=1536, y_cam=1024, test_list=camera_tests,
                          campos=campos, save_time=2.0)
    cameras.append(cam_right)
    campos = carla.Transform(carla.Location(x=0.55, y=-1.1, z=1.1), carla.Rotation(yaw=270.0, pitch=-20.0))
    cam_left = RGBCamera(cam_name="Left", x_cam=1536, y_cam=1024, test_list=camera_tests,
                         campos=campos, save_time=2.0)
    cameras.append(cam_left)

    test = CarlaTestRun(cameras, name=testname, spawn_point=spawn_point, ticks=cycles, folder=folder, tick_length=0.05,
                        town=town)
    test.run_texture(tsr_texture, ROUND_TRAFFIC_SIGNS_TOWN7)
    test.end()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("r", type=str, help="Filepath and name of the results directory")
    args = parser.parse_args()
    main(args.r)
