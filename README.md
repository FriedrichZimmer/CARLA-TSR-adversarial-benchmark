# Carla Attack Simulator

## Description
This project is for generating image material for testing automotive computer vision systems. It focuses on adversarial attacks on traffic sign recognition and lane detection. 
For this, adversarial examples from several publications were included into the carla Maps Town07 and Town10.
It is based on Carla 9.15 and its Python API.
This script can also be used for generating training images for new traffic sign recognition models.
The current version features:
- One map with adversarial examples for traffic sign recognition and lane detection
- A Tool that allows the creation of videos that serve as benchmark for the testing of CV Systems
- A collection of 15 textures of normal german traffic signs and 12 textures for adversarial examples
- Supports testing in different visibility conditions like bad camera settings or bad weather

![heavy rain](/images/visual.png)
Adversarial example at rainy weather


## Installation
This project was developed on Windows 11 and Python 3.10.
1. Install Carla 9.15 for Windows (Available on https://carla.org/2023/11/10/release-0.9.15/). Make sure that Carla is working properly on your computer.
2. Download the map Town07_attacked_09.15.2-1.zip from https://www.dropbox.com/scl/fi/jli3k8np295r0lgt23rvh/Town07_attacked_0.9.15.2-1.zip?rlkey=r8a54thl01lj1r80i6trn6fzo&st=1v9si945&dl=0
3. Unzip it and copy the content into the carla main folder (overwrite when needed).
4. Install the needed python frameworks with pip.
```
pip install numpy, carla, opencv-python, Pillow
```

## Usage
For generating image data, first start the Carla Simulation Server \WindowsNoEditor\CarlaUE4.exe

Then start one of the test scripts, for example
```
python test_town07_tsr_weather.py D:/Results
```
The script will generate several layers of folder in the format D:/Results/YYYYMMDD__hhmm_testname/trafficsign/camera
The resulting images will appear in those subfolders

There are also several smaller tools in the /tools folderthat can provide additional help:

camera_show_position.py:
This spawns a vehicle and several cameras attached to it. Then it shows the cameras in the map as arrows in the simulation.

convert_img_video.py:
This converts a folder full of images into a video, which will be stored in the subfolder /_video

map_data.py:
This lists all landmarks ad blueprints of the current map.

show_spawnpoints.py:
This shows all spawnpoints of the current map including their id in the simulator.

to_realtime.py:
This switches the current world back to realtime mode. This is useful in case a test got interrupted.

## Support
For small questions or requests, you can send an E-Mail to friedrich.zimmer@arrk-engineering.com.

My company, ARRK Engineering GmbH is an engineering service provider for the automotive industry.
So, for larger tasks, we can offer a more profound simulation or adaption to specific needs.

## Roadmap

Some ideas for the future:
- [ ] Implement Road Signs as actors instead of static objects. This way, also traffic signs with triangular or octogonal shapes can get spawned into a map instead of just using round ones.
- [ ] Adapt to the new Carla Version based on the Unreal 5 Engine based coming soon
- [ ] Add more road signs textures (Other german road signs, from different countries and additional adversarial examples)
- [ ] Depth camera to simulate Radar/Lidar.
- [ ] Live testing of CV Systems including feedback to simulation (like steering or exposure time settings)
- [ ] Fisheye postprocessing of images
- [ ] Using the ExperimentSuite functions of Carla

## Contributing
If you have got additional adversarial examples, I'm always interested in adding them. If you want to implement some ideas mentioned


## License
This project is licensed under the MIT license.
Copyright 2024 (c) Friedrich Zimmer at ARRK Engineering

## Project status
Until my Master Thesis is finsihed end of August 2024, I will continuously update this project. After this it depends on demand and on the time I have got available for implementing improvements.

***

