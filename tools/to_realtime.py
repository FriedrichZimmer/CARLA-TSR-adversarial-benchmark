"""
Copyright (c) 2024 Friedrich Zimmer
switching the simulator back to realtime mode, in case a test gor interuppted.
"""

import carla

client = carla.Client('127.0.0.1', 2000)
client.set_timeout(2.0)


# Once we have a client we can retrieve the world that is currently
# running.
world = client.get_world()

print('switching to rt mode')
settings = world.get_settings()
settings.synchronous_mode = False  # Enables synchronous mode
world.apply_settings(settings)
