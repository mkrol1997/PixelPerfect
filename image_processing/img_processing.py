import os
from io import BytesIO

import cv2
import numpy
from django.conf import settings
from PIL import Image

from FBCNN import fbcnn_color, fbcnn_color_real, fbcnn_gray
from image_processing.config import MODELS_STORAGE


class ImgProcesses:
    @staticmethod
    def img_read_from_memory(image_bytes: BytesIO) -> numpy.ndarray:
        image_bytes_array = numpy.asarray(bytearray(image_bytes.file.read()), dtype=numpy.uint8)
        img_obj = cv2.imdecode(image_bytes_array, cv2.IMREAD_COLOR)
        return img_obj

    @staticmethod
    def img_write_from_memory(image_bytes: BytesIO, save_to_path) -> Image:
        image = Image.open(image_bytes)
        orginal_image_path = os.path.join(save_to_path, image_bytes.name)

        image.save(orginal_image_path, optimize=True)

        return orginal_image_path

    @staticmethod
    def upscale_image(src_image_bytes: bytes, model: str, scale: int, save_to_path: str) -> str:
        src_img_name, img_extension = os.path.splitext(src_image_bytes.name)

        img = ImgProcesses.img_read_from_memory(src_image_bytes)

        requested_model = model + str(scale)
        model_object = MODELS_STORAGE[requested_model]

        super_res = cv2.dnn_superres.DnnSuperResImpl_create()
        super_res.readModel(model_object)
        super_res.setModel(model, scale)

        upscaled_image = super_res.upsample(img)

        upscaled_image_name = f"{src_img_name}-{model}_x{scale}{img_extension}"

        upscaled_image_path = os.path.join(save_to_path, upscaled_image_name)
        cv2.imwrite(upscaled_image_path, upscaled_image)

        return upscaled_image_path

    @staticmethod
    def compress_image(src_image_path: str, quality_factor: int) -> bool:
        orginal_image = Image.open(src_image_path)
        orginal_image.save(src_image_path, optimize=True, quality=int(quality_factor))

    @staticmethod
    def enhance_image(src_img, img_type, quality_factor, save_to_path):
        enhance_options = {
            "color": fbcnn_color.enhance,
            "color_real": fbcnn_color_real.enhance,
            "greyscale": fbcnn_gray.enhance,
        }

        image = ImgProcesses.img_write_from_memory(src_img, save_to_path)
        cnn_model = MODELS_STORAGE[img_type]

        params = {
            "src_image_path": image,
            "cnn_model": cnn_model,
            "save_to": save_to_path,
            "quality_factor": quality_factor,
        }

        enhanced_img = enhance_options[img_type](**params)

        return enhanced_img
