import os

import cv2
import numpy
from PIL import Image
from django.conf import settings


def compress(src_image, compress_to_format, quality_factor):
    compressed_image = Image.open(src_image)
    origin_image_name, extension = os.path.splitext(src_image.name)

    save_to_path = os.path.join(settings.BASE_DIR, 'media\\compressed_images')
    compressed_image_name = origin_image_name + 'compressed-' + extension
    compressed_image.save(
        os.path.join(save_to_path, compressed_image_name),
        compress_to_format,
        optimize=True,
        quality=10)

    return


def upscale_image(src_image, model, scale, user_id):
    models_storage = {
        'edsr2': os.path.join(settings.BASE_DIR.parent, 'image_processing/models/upscale/EDSR/EDSR_x2.pb'),
        'edsr3': os.path.join(settings.BASE_DIR.parent, 'image_processing/models/upscale/EDSR/EDSR_x3.pb'),
        'edsr4': os.path.join(settings.BASE_DIR.parent, 'image_processing/models/upscale/EDSR/EDSR_x4.pb'),
        'espcn2': os.path.join(settings.BASE_DIR.parent, 'image_processing/models/upscale/ESPCN/ESPCN_x2.pb'),
        'espcn3': os.path.join(settings.BASE_DIR.parent, 'image_processing/models/upscale/ESPCN/ESPCN_x3.pb'),
        'espcn4': os.path.join(settings.BASE_DIR.parent, 'image_processing/models/upscale/ESPCN/ESPCN_x4.pb'),
        'fsrcnn2': os.path.join(settings.BASE_DIR.parent, 'image_processing/models/upscale/FSRCNN/FSRCNN_x2.pb'),
        'fsrcnn3': os.path.join(settings.BASE_DIR.parent, 'image_processing/models/upscale/FSRCNN/FSRCNN_x3.pb'),
        'fsrcnn4': os.path.join(settings.BASE_DIR.parent, 'image_processing/models/upscale/FSRCNN/FSRCNN_x4.pb'),
        'lapsrn2': os.path.join(settings.BASE_DIR.parent, 'image_processing/models/upscale/LapSRN/LapSRN_x2.pb'),
        'lapsrn4': os.path.join(settings.BASE_DIR.parent, 'image_processing/models/upscale/LapSRN/LapSRN_x4.pb'),
        'lapsrn8': os.path.join(settings.BASE_DIR.parent, 'image_processing/models/upscale/LapSRN/LapSRN_x8.pb'),
    }

    origin_image_name, extension = os.path.splitext(src_image.name)
    origin_image = numpy.asarray(bytearray(src_image.file.read()), dtype=numpy.uint8)
    img = cv2.imdecode(origin_image, cv2.IMREAD_COLOR)

    requested_model = model + str(scale)
    model_object = models_storage[requested_model]

    super_res = cv2.dnn_superres.DnnSuperResImpl_create()
    super_res.readModel(model_object)
    super_res.setModel(model, scale)

    result_image = super_res.upsample(img)

    upscaled_image_name = f'{origin_image_name}-{model}_x{scale}{extension}'
    save_to_dir_path = os.path.join(settings.BASE_DIR, 'media\\upscaled_images\\')

    image_path = os.path.join(save_to_dir_path, upscaled_image_name)
    cv2.imwrite(image_path, result_image)

    return image_path
