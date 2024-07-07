"""
Copyright (c) 2024 Friedrich Zimmer
defines several weather conditions that can be used in various tests
"""

import carla


def heavy_rain():
    return carla.WeatherParameters(
        cloudiness=80.0,
        precipitation=100.0,
        precipitation_deposits=40.0,
        wind_intensity=30.0,
        sun_azimuth_angle=285,
        sun_altitude_angle=25,
        fog_density=10.0,
        fog_distance=60.0,
        fog_falloff=1.0,
        wetness=100.0,
        scattering_intensity=1.0,
        mie_scattering_scale=0.03,
        rayleigh_scattering_scale=0.0331
    )


def foggy():
    return carla.WeatherParameters(
        cloudiness=90,
        precipitation=0.0,
        precipitation_deposits=40.0,
        wind_intensity=30.0,
        sun_azimuth_angle=285,
        sun_altitude_angle=25,
        fog_density=100.0,
        fog_distance=0.0,
        fog_falloff=1.0,
        wetness=0.0,
        scattering_intensity=1.0,
        mie_scattering_scale=0.03,
        rayleigh_scattering_scale=0.0331
    )


def sunset(sun_direction, altitude=1.6):
    return carla.WeatherParameters(
        cloudiness=10.0,
        precipitation=0.0,
        precipitation_deposits=40.0,
        wind_intensity=30.0,
        sun_azimuth_angle=sun_direction,
        sun_altitude_angle=altitude,
        fog_density=10.0,
        fog_distance=60.0,
        fog_falloff=1.0,
        wetness=0.0,
        scattering_intensity=1.0,
        mie_scattering_scale=0.03,
        rayleigh_scattering_scale=0.0331
    )


def town7_default():
    return carla.WeatherParameters(
        cloudiness=10.0,
        precipitation=0.0,
        precipitation_deposits=40.0,
        wind_intensity=30.0,
        sun_azimuth_angle=285,
        sun_altitude_angle=25,
        fog_density=10.0,
        fog_distance=60.0,
        fog_falloff=1.0,
        wetness=0.0,
        scattering_intensity=1.0,
        mie_scattering_scale=0.03,
        rayleigh_scattering_scale=0.0331
    )


if __name__ == '__main__':
    # manually changing weather
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    # world.set_weather(heavy_rain())
    world.set_weather(town7_default())
