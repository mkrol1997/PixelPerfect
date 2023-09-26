import os

from django.conf import settings

upscaled_img_path = os.path.join(settings.BASE_DIR, "media/upscaled_images/")
enhanced_img_path = os.path.join(settings.BASE_DIR, "media/enhanced_images/")


MODELS_STORAGE = {
    "edsr2": os.path.join(settings.BASE_DIR, "image_processing/models/upscale/EDSR/EDSR_x2.pb"),
    "edsr3": os.path.join(settings.BASE_DIR, "image_processing/models/upscale/EDSR/EDSR_x3.pb"),
    "edsr4": os.path.join(settings.BASE_DIR, "image_processing/models/upscale/EDSR/EDSR_x4.pb"),
    "espcn2": os.path.join(settings.BASE_DIR, "image_processing/models/upscale/ESPCN/ESPCN_x2.pb"),
    "espcn3": os.path.join(settings.BASE_DIR, "image_processing/models/upscale/ESPCN/ESPCN_x3.pb"),
    "espcn4": os.path.join(settings.BASE_DIR, "image_processing/models/upscale/ESPCN/ESPCN_x4.pb"),
    "fsrcnn2": os.path.join(settings.BASE_DIR, "image_processing/models/upscale/FSRCNN/FSRCNN_x2.pb"),
    "fsrcnn3": os.path.join(settings.BASE_DIR, "image_processing/models/upscale/FSRCNN/FSRCNN_x3.pb"),
    "fsrcnn4": os.path.join(settings.BASE_DIR, "image_processing/models/upscale/FSRCNN/FSRCNN_x4.pb"),
    "lapsrn2": os.path.join(settings.BASE_DIR, "image_processing/models/upscale/LapSRN/LapSRN_x2.pb"),
    "lapsrn4": os.path.join(settings.BASE_DIR, "image_processing/models/upscale/LapSRN/LapSRN_x4.pb"),
    "lapsrn8": os.path.join(settings.BASE_DIR, "image_processing/models/upscale/LapSRN/LapSRN_x8.pb"),
    "color": os.path.join(settings.BASE_DIR, "image_processing/models/enhance/fbcnn_color.pth"),
    "color_real": os.path.join(settings.BASE_DIR, "image_processing/models/enhance/fbcnn_color.pth"),
    "greyscale": os.path.join(settings.BASE_DIR, "image_processing/models/enhance/fbcnn_gray.pth"),
}
