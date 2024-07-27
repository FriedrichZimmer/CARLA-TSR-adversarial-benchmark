"""Copyright (c) 2024 Friedrich Zimmer
RGB Camera Class and standard setings used by all tests.
"""
import logging
from time import sleep

import carla
import os
from util.test_class import cam_lambda


# list of all camera tests
camera_tests = ['00_default_carla',
                '01_default_new',
                '02_auto_exposure',
                '10_mblur_low',
                '11_mblur_high',
                '20_low_shutter_speed',
                '21_high_shutter_speed',
                '22_low_shutter_speed_iso',
                '23_high_shutter_speed_iso',
                '30_iso_400',
                '31_iso_25',
                '40_high_gamma',
                '41_gamma_1.0',
                '50_high_lensflare_intensity',
                '60_small_f_stop',
                '61_large_fstop',
                '62_small_f_stop_iso',
                '63_large_fstop_iso',
                '70_npp'
                ]


def set_camera_test(test, camera_bp):
    """ settings of all camera tests """
    if test == '00_default_carla':
        # changing back to carla default
        camera_bp.set_attribute('exposure_mode', 'histogramm')
        camera_bp.set_attribute('gamma', '2.2')
    elif test == '01_default_new':
        pass
    elif test == '02_auto_exposure':
        camera_bp.set_attribute('exposure_mode', 'histogramm')
    elif test == '10_mblur_low':
        camera_bp.set_attribute('blur_amount', '0.3')
        camera_bp.set_attribute('motion_blur_intensity', '0.2')
        camera_bp.set_attribute('motion_blur_max_distortion', '0.15')
        camera_bp.set_attribute('motion_blur_min_object_screen_size', '0.04')
    elif test == '11_mblur_high':
        camera_bp.set_attribute('blur_amount', '3.5')
        camera_bp.set_attribute('motion_blur_intensity', '0.8')
        camera_bp.set_attribute('motion_blur_max_distortion', '0.7')
        camera_bp.set_attribute('motion_blur_min_object_screen_size', '0.4')
    elif test == '20_low_shutter_speed':
        camera_bp.set_attribute('shutter_speed', '50.0')
    elif test == '21_high_shutter_speed':
        camera_bp.set_attribute('shutter_speed', '800.0')
    elif test == '22_low_shutter_speed_iso':
        camera_bp.set_attribute('shutter_speed', '50.0')
        camera_bp.set_attribute('iso', '25')
    elif test == '23_high_shutter_speed_iso':
        camera_bp.set_attribute('shutter_speed', '800.0')
        camera_bp.set_attribute('iso', '400')
    elif test == '30_iso_400':
        camera_bp.set_attribute('iso', '400')
    elif test == '31_iso_25':
        camera_bp.set_attribute('iso', '25')
    elif test == '32_npp_iso1600':
        camera_bp.set_attribute('enable_postprocess_effects', 'False')
        camera_bp.set_attribute('iso', '400')
    elif test == '40_high_gamma':
        camera_bp.set_attribute('gamma', '5.0')
    elif test == '50_high_lensflare_intensity':
        camera_bp.set_attribute('lens_flare_intensity', '1.5')
    elif test == '60_small_f_stop':
        camera_bp.set_attribute('fstop', '0.7')
    elif test == '61_large_fstop':
        camera_bp.set_attribute('fstop', '2.8')
    elif test == '62_small_f_stop_iso':
        camera_bp.set_attribute('fstop', '0.7')
        camera_bp.set_attribute('iso', '25')
    elif test == '63_large_fstop_iso':
        camera_bp.set_attribute('fstop', '2.8')
        camera_bp.set_attribute('iso', '400')
    elif test == '70_distort_lens_circle_falloff_1':
        camera_bp.set_attribute('lens_circle_falloff', '1.0')
    elif test == '71_distort_lens_circle_falloff_9':
        camera_bp.set_attribute('lens_circle_falloff', '9.0')
    elif test == '72_lens_circle_multiplier_5':
        camera_bp.set_attribute('lens_circle_multiplier', '5.0')
    elif test == '73_lens_k_-10':
        camera_bp.set_attribute('lens_k', '-10.0')
    elif test == '74_lens_k_10':
        camera_bp.set_attribute('lens_k', '10.0')
    elif test == '75_lens_kcube_-10':
        camera_bp.set_attribute('lens_kcube', '-10.0')
    elif test == '76_lens_kcube_10':
        camera_bp.set_attribute('lens_kcube', '10.0')
    elif test == '80_lens_circle_multiplier_1':
        camera_bp.set_attribute('lens_circle_multiplier', '1.0')
    elif test == '81_lens_circle_multiplier_2':
        camera_bp.set_attribute('lens_circle_multiplier', '2.0')
    elif test == '82_lens_circle_multiplier_10':
        camera_bp.set_attribute('lens_circle_multiplier', '10.0')

    else:
        print('WARNING! Unknown settings: ' + test)


class RGBCamera:
    """class for cameras. Needs to be defined before testing and then submitted to the CarlaTestRun Object"""

    def __init__(self, cam_name="", x_cam=1360, y_cam=800, fov=120, tick=0.0, test_list=None,
                 campos=carla.Transform(carla.Location(x=0.6, z=1.45)), save_time=0.25):
        """Init with camera configuration data. Standard resolution is the same as in the GTSRDB dataset

        Args:
            x_cam (int): x resolution of the camera
            y_cam (int): y resolution of the camera
            fov (int): field of view of the camera in degrees
            tick (float): time between images (= 1/framerate) 0.0 means its synchronous with the world tick
            test_list ([str]): list of camera settings
            campos (Location): position of the camera in relation to the vehicle
            save_time (float): sleep time used for saving images inbetween ticks
        """
        self.x_cam = x_cam
        self.y_cam = y_cam
        self.fov = fov
        self.sensor_tick = tick
        if test_list is None:
            self.test_list = ['01_default_new']
        else:
            self.test_list = test_list
        self.transform = campos
        self.save_time = save_time
        if cam_name != "":
            cam_name = cam_name + "_"
        self.cam_name = cam_name

        self.cameras = []
        self.logger = logging.getLogger('logger')

    def log_basic_info(self, logger=None):
        """receives the logger from the Test script and logs the used camera settings"""
        if logger:
            self.logger = logger
        self.logger.info(f'Resulution: {self.x_cam}x{self.y_cam}')
        self.logger.info(f'FOV: {self.fov}°')
        self.logger.info(f'Sensor_Tick: {self.sensor_tick} seconds')
        self.logger.info(f'List of cameras: {self.test_list}')

    def setup_rgb_camera(self, blueprint_library, i):
        """Creates and configures a single camera based on the carla Blueprint

        Args:
            blueprint_library: Blueprint library of the current map
            i (int): Iterator for the list of cameras

        Returns:
            camera_bp (BluePrint): RGB Camera with the desired settings
        """
        if i > len(self.test_list)-1:
            self.logger.error(f'Camera does not exist. Switching to default. ' + str(i))
            i = 0

        self.logger.info('Camera:' + self.test_list[i])
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', str(self.x_cam))
        camera_bp.set_attribute('image_size_y', str(self.y_cam))
        camera_bp.set_attribute('fov', str(self.fov))
        camera_bp.set_attribute('sensor_tick', str(self.sensor_tick))
        camera_bp.set_attribute('exposure_mode', 'manual')
        camera_bp.set_attribute('gamma', '1.0')
        set_camera_test(self.test_list[i], camera_bp)

        return camera_bp

    def attach_cameras(self, world, vehicle, test_folder):
        """Creates all cameras and attach them to the vehicle

        Args:
            world (World): The currently loaded map
            vehicle (Actor): The spawned vehicle where the camera needs to be attached
            test_folder (str): location for storing the resulting image
        """
        blueprint_library = world.get_blueprint_library()
        for i in range(0, len(self.test_list)):
            # prepare the camera blueprint
            camera_bp = self.setup_rgb_camera(blueprint_library, i)
            # spawn and attach the camera
            camera = world.spawn_actor(camera_bp, self.transform, attach_to=vehicle)
            self.cameras.append(camera)
            # create folder for resulting images
            cam_folder = os.path.join(test_folder, self.cam_name + self.test_list[i])
            if not os.path.exists(cam_folder):
                self.logger.info(f'Creating folder: {cam_folder}')
                os.makedirs(cam_folder)
            # camera listener
            target_file = lambda image, img_path=cam_folder, t=(i * self.save_time): (cam_lambda(image, img_path, t, self.logger))
            camera.listen(target_file)

    def destroy_all(self):
        """Destroys cameras after test to avoid memory leak"""
        self.logger.info(f'Destroying {len(self.cameras)} cameras')
        for camera in self.cameras:
            camera.destroy()
        self.cameras = []

    def tick_sleep(self):
        sleep(self.save_time * len(self.test_list))
