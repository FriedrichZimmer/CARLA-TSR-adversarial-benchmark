"""
Copyright (c) 2024 Friedrich Zimmer
shows position of the cameras in the map on a standing vehicle
"""

import glob
import os
import sys

from util.camera_utils import setup_rgb_camera

import carla

import random
from time import strftime, localtime, sleep

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

testname = 'camera_setting_test'
RESULT_FOLDER = os.path.join( 'D:/Results/', strftime('%Y%m%d_%H%M', localtime()) + '_' + testname)
print(RESULT_FOLDER)

spawn_point = 20
wait_between_tick = 0.4
tick = 0.01

# camera options
x_cam = 1920
y_cam = 1080
sensor_tick = 0.01
fov = 120


def main():
    """connects to server and shows 5 camea positions as red arrows directly in the simulation.
    Arrows automatically disappear after 40 seconds"""
    actor_list = []
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(2.0)

    world = client.get_world()

    print('switching to sync mode')
    settings = world.get_settings()

    world.apply_settings(settings)
    blueprint_library = world.get_blueprint_library()
    bp_vehicle = blueprint_library.find('vehicle.bmw.grandtourer')
    if bp_vehicle.has_attribute('color'):
        color = random.choice(bp_vehicle.get_attribute('color').recommended_values)
        print(color)
        bp_vehicle.set_attribute('color', color)

    transform = world.get_map().get_spawn_points()[spawn_point]
    print(transform.location)

    vehicle = world.spawn_actor(bp_vehicle, transform)
    actor_list.append(vehicle)

    # move spectator to car
    transform.location.z = 2
    spectator = world.get_spectator()
    spectator.set_transform(transform)

    # load camera bp
    camera_bp = setup_rgb_camera(blueprint_library, x_cam, y_cam, fov, sensor_tick)
    camera_transform = carla.Transform(carla.Location(x=0.5, z=1.42))
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
    actor_list.append(camera)

    c2_transform = carla.Transform(carla.Location(x=2.35, z=0.4))
    camera2 = world.spawn_actor(camera_bp, c2_transform, attach_to=vehicle)
    actor_list.append(camera2)

    c3_transform = carla.Transform(carla.Location(x=-2.3, z=0.4), carla.Rotation(yaw=180.0))
    camera3 = world.spawn_actor(camera_bp, c3_transform, attach_to=vehicle)
    actor_list.append(camera2)

    c4_transform = carla.Transform(carla.Location(x=0.55, y=1.1, z=1.1), carla.Rotation(yaw=90.0))
    camera4 = world.spawn_actor(camera_bp, c4_transform, attach_to=vehicle)
    actor_list.append(camera2)

    c5_transform = carla.Transform(carla.Location(x=0.55, y=-1.1, z=1.1), carla.Rotation(yaw=270.0))
    camera5 = world.spawn_actor(camera_bp, c5_transform, attach_to=vehicle)
    actor_list.append(camera2)

    # dropping time for the vehicle
    sleep(2)

    print(f'Printing arrow at {camera_transform.location}')

    # get location and rotation of the Camera objects
    ct = camera.get_transform()
    print(str(ct))
    ct2 = camera2.get_transform()
    print(str(ct2))
    ct3 = camera3.get_transform()
    print(str(ct3))
    ct4 = camera4.get_transform()
    print(str(ct3))
    ct5 = camera5.get_transform()
    print(str(ct3))

    # draw arrows in simulation
    world.debug.draw_arrow(ct.location, ct.location + 0.7*ct.get_forward_vector(), thickness=0.03, life_time=40)
    world.debug.draw_arrow(ct2.location, ct2.location + 0.7*ct2.get_forward_vector(), thickness=0.03, life_time=40)
    world.debug.draw_arrow(ct3.location, ct3.location + 0.7*ct3.get_forward_vector(), thickness=0.03, life_time=40)
    world.debug.draw_arrow(ct4.location, ct4.location + 0.7*ct4.get_forward_vector(), thickness=0.03, life_time=40)
    world.debug.draw_arrow(ct5.location, ct5.location + 0.7*ct5.get_forward_vector(), thickness=0.03, life_time=40)

    sleep(40)

    client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])

    print('done.')


if __name__ == '__main__':
    main()
