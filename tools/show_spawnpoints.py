"""
Copyright (c) 2024 Friedrich Zimmer
show all spawn point IDs in the simulation. This is a tool"""

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
import time


def show_spawnpoints():
    """show all spawn point IDs of the current map in the simulation"""

    try:
        # Create Client
        client = carla.Client('127.0.0.1', 2000)
        client.set_timeout(2.0)
        world = client.get_world()

        # Get the map spawn points
        spawn_points = world.get_map().get_spawn_points()

        print('Showing spawn points in Simulation for 100 seconds')

        for i, spawn_point in enumerate(spawn_points):
            # Draw in the spectator window the spawn point ID
            world.debug.draw_string(spawn_point.location, str(i), life_time=100)
            # draw direction arrow
            world.debug.draw_arrow(spawn_point.location, spawn_point.location + spawn_point.get_forward_vector(),
                                   life_time=100)
        time.sleep(10)

    finally:
        print('done.')


if __name__ == '__main__':

    show_spawnpoints()
