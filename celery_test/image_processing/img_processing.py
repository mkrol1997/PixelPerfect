import os

import cv2
import numpy
from django.core.files.uploadhandler import InMemoryUploadedFile
from PIL import Image
from django.conf import settings
from FBCNN import fbcnn_color, fbcnn_color_real, fbcnn_gray
from .config import MODELS_STORAGE


class ImgProcesses:
    @staticmethod
    def img_read_from_memory(image_bytes: InMemoryUploadedFile) -> numpy.ndarray:
        image_bytes_array = numpy.asarray(bytearray(), dtype=numpy.uint8)
        img_obj = cv2.imdecode(image_bytes_array, cv2.IMREAD_COLOR)

        return img_obj

    @staticmethod
    def img_write_from_memory(image_bytes: InMemoryUploadedFile, save_to_path) -> str:
        image = Image.open(image_bytes)

        original_image_path = os.path.join(save_to_path, image_bytes.name)
        image.save(original_image_path)

        return original_image_path

    @staticmethod
    def upscale_image(src_image_path: str, model: str, scale: int) -> str:
        model_object = MODELS_STORAGE[model + str(scale)]

        super_res = cv2.dnn_superres.DnnSuperResImpl_create()
        super_res.readModel(model_object)
        super_res.setModel(model, scale)

        image = cv2.imread(src_image_path)

        upscaled = super_res.upsample(image)

        cv2.imwrite(src_image_path, upscaled)

        return src_image_path

        # image = cv2.imread(src_image_path)
        #
        # requested_model = model + str(scale)
        # model_object = MODELS_STORAGE[requested_model]
        #
        # super_res = cv2.dnn_superres.DnnSuperResImpl_create()
        # super_res.readModel(model_object)
        # super_res.setModel(model, scale)
        #
        # super_res.upsample(image)
        #
        # cv2.imwrite(src_image_path, upscaled_image)
        #
        # return src_image_path

    @staticmethod
    def compress_image(src_image_path: str, quality_factor: int):
        original_image = Image.open(src_image_path)
        original_image.save(src_image_path, optimize=True, quality=int(quality_factor))

    @staticmethod
    def enhance_image(src_img, img_type, quality_factor, save_to_path):
        enhance_operations = {
            "color": fbcnn_color.enhance,
            "color_real": fbcnn_color_real.enhance,
            "greyscale": fbcnn_gray.enhance,
        }

        if isinstance(src_img, InMemoryUploadedFile):
            image = ImgProcesses.img_write_from_memory(src_img, save_to_path)
        else:
            image = src_img

        cnn_model = MODELS_STORAGE[img_type]

        operation_params = {
            "src_image_path": image,
            "cnn_model": cnn_model,
            "save_to": save_to_path,
            "quality_factor": quality_factor,
        }

        enhanced_img = enhance_operations[img_type](**operation_params)

        return enhanced_img
