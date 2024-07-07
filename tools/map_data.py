"""
Copyright (c) 2024 Friedrich Zimmer
"""
from argparse import ArgumentParser

import carla


def map_data(load_map=None):
    """listing all blueprints, landmarks and objects of the current world/map.
    Can also be used to load a specified map before."""
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(3.0)

    print(f'Available Maps:\n{client.get_available_maps()}')

    world = None
    if load_map:
        print(f'now loading map {load_map}')
        world = client.load_world_if_different(load_map, reset_settings=True)
    if not world:
        print(f'Getting World Data')
        world = client.get_world()

    print('\n\nVehicle Blueprints:')
    blueprint_library = world.get_blueprint_library().filter('vehicle')
    for item in blueprint_library:
        print(f'{item.id}, {item.tags[0]}, {item.tags[1]}, {item.tags[2]}')

    print('\n\nStatic Blueprints:')
    blueprint_library = world.get_blueprint_library().filter('static')
    for item in blueprint_library:
        print(f'{item.id}, {item.tags[0]}, {item.tags[1]}, {item.tags[2]}')

    print('\n\nLandmarks:')
    landmarks = world.get_map().get_all_landmarks()
    for landmark in landmarks:
        print(f'{landmark.id}, {landmark.name}, {landmark.country}, {landmark.is_dynamic}, {landmark.type}')

    print('\n\nObjects:')
    objects = world.get_names_of_all_objects()
    for carla_object in objects:
        print(str(carla_object))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-map', type=str, help='Load a certain map before reading the data')
    args = parser.parse_args()
    map_data(args.map)
