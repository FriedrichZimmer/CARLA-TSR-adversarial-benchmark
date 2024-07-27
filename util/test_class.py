"""
Copyright (c) 2024 Friedrich Zimmer
Test Class used by all tests
"""

import glob
import os
import sys
import carla
import logging
from time import strftime, localtime, sleep
from util.update_texture import update_texture

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

current_tick = 0


# logger = logging.getLogger(__name__)


def cam_lambda(image, img_path, t, logger):
    """in order to avoid that all cameras try to save their pictures at once.
    Needs to be in test definition for global variable.Is used by camera lambda

    Args:
        image (Image): image that was created by a camera
        img_path (str): path to store the resulting image
        t: (float) sleep time in seconds
        logger (Logger): Logger object for showing and recording the progress
        """

    global current_tick
    img = f'{img_path}/{current_tick:04d}.png'
    # sleep time to give the background processes enough time to store the image of the other images of the same tick
    # on the hard disk
    sleep(t)
    image.save_to_disk(img)
    logger.info(f'Saved {img}')


def carla_init(tick, logger, town=None):
    """for connecting to a client and initiating the map

    Args:
        tick (float): tick time of the world in seconds
        logger (Logger): Logger object for showing and recording the progress
        town (str): Name of the test town to make sure the correct map is loaded before starting the test
    """
    client = carla.Client('127.0.0.1', 2000)
    # long timeout of 15 seconds is needed for loading a different world. (Might be even longer for slower computers)
    client.set_timeout(15.0)
    if town:
        # change map if a certain map has been demanded
        logger.info(f'Loading map {town}...')
        world = client.load_world_if_different(town, reset_settings=True)
        # load_world_if_different returns none, if the desired world is already loaded. In this case
        if not world:
            world = client.get_world()
    else:
        world = client.get_world()
    logger.info('Client connected. Switching to sync mode...')
    settings = world.get_settings()
    settings.synchronous_mode = True  # Enables synchronous mode
    settings.fixed_delta_seconds = tick
    world.apply_settings(settings)
    # connect to the traffic manager
    tm = client.get_trafficmanager(8000)
    tm.set_synchronous_mode(True)

    return world, tm


class CarlaTestRun:
    """This is the main class for performing a test with carla. The result is folder with subfolders full of images"""

    def __init__(self, cameras, name='generic_test', folder='D:/Results/', spawn_point=79, ticks_prep=50, ticks=200,
                 tick_length=0.05, town=None):
        """ Initiates and configures a Testrun

        Args:
            cameras ([Camera]): Array of Camera objects that defines all cameras that will be added to the vehicle
            name (str): Test name will be used for labeling the directory
            folder (str): Basic folder for test results
            spawn_point (int): ID of the spawn point of the vehicle in the current map
            ticks_prep (int): Amount of ticks for accelerating the vehicle before the recording starts
            ticks (int): Amount of world ticks when the recording is happening
            tick_length (float): Length of a world tick in seconds
            town (str): Name of the test town to make sure the correct map is loaded before starting the test
        """
        self.cameras = cameras
        self.name = name
        # self.spawn_point = spawn_point
        self.ticks_prep = ticks_prep
        self.ticks = ticks
        self.tick_length = tick_length
        self.result_folder = self.init_result_folder(folder)
        self.spawn_point = spawn_point
        self.logger = self.start_logging()
        self.world, self.tm = carla_init(tick_length, self.logger, town)
        self.spawn_location = self.spawn_transform()
        self.bp_vehicle = self.gen_vehicle_bp()

    def start_logging(self):
        """creates a logger that will log to both screen and logfile

        Returns:
            logger: A Logging object
        """

        # Setting up the logger
        logger = logging.getLogger('logger')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        logfile = os.path.join(self.result_folder, 'log' + strftime('%Y%m%d_%H%M', localtime()) + '.log')
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Logging the Specification of the current test
        logger.info(self.name)
        logger.info(self.result_folder)
        logger.info(f'Spawn Point: {self.spawn_point}')
        logger.info(f'Preparation Ticks: {self.ticks_prep}')
        logger.info(f'Recording Ticks: {self.ticks}')
        logger.info(f'Ticks: {self.tick_length} Seconds')
        for cam in self.cameras:
            cam.log_basic_info(logger)
        return logger

    def spawn_transform(self):
        """returns the transform of the spawn location and also moves the spectator there"""
        spawn_location = self.world.get_map().get_spawn_points()[self.spawn_point]
        self.logger.info(f'Vehicle spawn point: {spawn_location.location}')
        # move spectator to car (only in first cycle)
        spawn_location.location.z = 2
        spectator = self.world.get_spectator()
        spectator.set_transform(spawn_location)
        spawn_location.location.z = 1.5
        return spawn_location

    def init_result_folder(self, folder):
        """
        Generates Result folder in the basic folder

        Args:
            folder: String where the folder for the results of the current test have to be created

        Returns:
            result_folder: String of the path of the result folder
        """
        result_folder = os.path.join(folder, strftime('%Y%m%d_%H%M', localtime()) + "_" + self.name)
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
        return result_folder

    def set_weather(self, weather):
        """
        function for setting the weather of the current map

        Args:
            weather: Weather object that defines the detailed weather conditions
        """
        self.world.set_weather(weather)
        self.logger.info('Weather changed')

    def single_test_cycle(self, test_cycle_name='Default'):
        """ create subfolder for results

        Args:
            test_cycle_name: String for labeling the result folder
        """
        test_folder = os.path.join(self.result_folder, test_cycle_name)
        if not os.path.exists(test_folder):
            os.makedirs(test_folder)

        # Spawning new vehicle at spawn point
        self.logger.info('Spawning new vehicle at spawn point')
        vehicle = self.world.spawn_actor(self.bp_vehicle, self.spawn_location)
        # car starts accelerating to 1 m/s
        vehicle.set_autopilot(True, self.tm.get_port())
        self.tm.set_desired_speed(vehicle, 36.0)
        self.tm.ignore_signs_percentage(vehicle, 100.0)
        # Some ticks to accelerate the vehicle
        self.logger.info(f'Accelerating vehicle for {self.ticks_prep} ticks')
        for i in range(0, self.ticks_prep):
            self.world.tick()
            sleep(self.tick_length)
        sleep(1)

        for cam in self.cameras:
            cam.attach_cameras(self.world, vehicle, test_folder)

        # testcycle
        global current_tick
        for current_tick in range(0, self.ticks):
            self.logger.info(f'Tick {current_tick} Speed {vehicle.get_velocity().length()} m/s')
            self.world.tick()
            # camera threads need time to save images
            self.cameras[0].tick_sleep()

        # give the camera threads enough time to save the images
        sleep(10)

        for cam in self.cameras:
            cam.destroy_all()
        self.logger.info('destroy vehicle')
        vehicle.destroy()

    def update_object_textures(self, image_path, objects):
        # paint traffic sign on sign.
        self.logger.info(f'Applying Texture {image_path} to objects')
        for o in objects:
            update_texture(self.world, o, image_path, self.logger)

    def run_texture(self, textures, objects):
        for tex in textures:
            self.update_object_textures(tex[1], objects)
            self.single_test_cycle(tex[0])

    def gen_vehicle_bp(self):
        # setting up vehicle
        blueprint_library = self.world.get_blueprint_library()
        bp_vehicle = blueprint_library.find('vehicle.bmw.grandtourer')
        if bp_vehicle.has_attribute('color'):
            color = bp_vehicle.get_attribute('color').recommended_values[0]
            bp_vehicle.set_attribute('color', color)
        return bp_vehicle

    def end(self):
        self.logger.info('switch back to real time mode')
        settings = self.world.get_settings()
        settings.synchronous_mode = False
        self.world.apply_settings(settings)
        self.logger.info('Test finished')
        print('Test finished')
