"""
Copyright (c) 2024 Friedrich Zimmer
scripts and lists for texture management of traffic signs
"""

from PIL import Image
import carla

# the texture files you can apply to round texture_objects. The names have to be the same as in the classifier labels
# of the tsr-collection repository
TS_TEXTURE_CIRCLE = [
    ['Speed_30', 'images\\textures_traffic_sign\\tempo30_512.png'],
    ['Speed_40', 'images\\textures_traffic_sign\\tempo40_512.png'],
    ['Speed_50', 'images\\textures_traffic_sign\\tempo50_512.png'],
    ['Speed_60', 'images\\textures_traffic_sign\\tempo60_512.png'],
    ['Speed_80', 'images\\textures_traffic_sign\\tempo80_512.png'],
    ['Speed_100', 'images\\textures_traffic_sign\\tempo100_512.png'],
    ['Speed_120', 'images\\textures_traffic_sign\\tempo120_512.png'],
    ['No_Entry', 'images\\textures_traffic_sign\\Verbot_Einf_512.png'],
    ['No_Vehicles', 'images\\textures_traffic_sign\\Verbot_alle_512.png'],
    ['No_Over', 'images\\textures_traffic_sign\\Uehvb_alle_512.png'],
    ['No_Over_Heavy', 'images\\textures_traffic_sign\\Uehvb_u2,8_512.png'],
    ['No_Parking', 'images\\textures_traffic_sign\\Eg_Hvb.png'],
    ['Ahead_Only', 'images\\textures_traffic_sign\\straight_ahead_512.png'],
    ['Speed_80_End', 'images\\textures_traffic_sign\\ende80_512.png'],
    ['Speed_60#Speed_50', 'images\\textures_traffic_sign\\morg_60_50.png'],
    ['Speed_50#Speed_30', 'images\\textures_traffic_sign\\morg_50_30.png'],
    ['Speed_80#Speed_60', 'images\\textures_traffic_sign\\morg_80_60.png'],
    ['Speed_100#Speed_120', 'images\\textures_traffic_sign\\morg_100_120.png'],
    ['Speed_30#Yield', 'images\\textures_traffic_sign\\sita_30_yield.png'],
    ['Speed_120#Speed_30', 'images\\textures_traffic_sign\\sita_120-30.png'],
    ['Speed_60#Speed_120', 'images\\textures_traffic_sign\\woit_60_120.png'],
    ['KFC#Stop', 'images\\textures_traffic_sign\\sita_kfc_stop.png'],
    ['Texaco#No_Over', 'images\\textures_traffic_sign\\sita_texaco_uebvb.png'],
    ['Speed_100#Speed_40', 'images\\textures_traffic_sign\\tempo100#40-wei_512.png'],
    ['Speed_40#Speed_60', 'images\\textures_traffic_sign\\jia_40_60.png']
]

# In a later version there can also be a test for stop signs and other octagonal texture objects.
TS_TEXTURE_OCTO = [[]]

# map specific street signs. Only usable for tests in World Town7_attacked
ROUND_TRAFFIC_SIGNS_TOWN7 = [
    'BP_Tempo64_2',
    'BP_Tempo65_5',
    'BP_Tempo66_8',
    'BP_Tempo67_11',
    'BP_Tempo68_14',
    'BP_Tempo69_17',
    'BP_Tempo70_2',
    'BP_Tempo71_5',
    'BP_Tempo72_2',
    'BP_Tempo73_5',
    'BP_Tempo74_8',
    'BP_Tempo75_11',
    'BP_Tempo76_14',
    'BP_Tempo77_17'
]


def update_texture(world, obj, imgfile, logger):
    """ uploading and updating the texture of a blueprint during runtime.
    Material of that object needs to be a Material instance of M_Materialmaster """

    logger.info('Texture applying ' + imgfile + ' to ' + obj)
    image = Image.open(imgfile)
    h = image.size[1]
    w = image.size[0]

    texture = carla.TextureColor(w, h)

    for x in range(0, w):
        for y in range(0, h):
            color = image.getpixel((x, y))
            # color = image[x, y]
            r = int(color[0])
            g = int(color[1])
            b = int(color[2])
            # alpha channel from original image is ignored. Instead, max opacity is applied
            a = 255
            texture.set(x, y, carla.Color(r, g, b, a))

    world.apply_color_texture_to_object(obj, carla.MaterialParameter.Diffuse, texture)
    # the following could be used if also a texture for other effect needs to be applied
    # world.apply_color_texture_to_object(obj, carla.MaterialParameter.Normal, texture)
    # world.apply_color_texture_to_object(obj, carla.MaterialParameter.AO_Roughness_Metallic_Emissive, texture)
