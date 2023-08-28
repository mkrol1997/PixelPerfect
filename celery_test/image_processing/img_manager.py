import os

from django.conf import settings

from image_processing.img_processing import ImgProcesses


class ImageManager:
    upscaled_img_path = os.path.join(settings.BASE_DIR, "media/upscaled_images/")
    enhanced_img_path = os.path.join(settings.BASE_DIR, "media/enhanced_images/")

    @staticmethod
    def upscale_image(src_image_path: str, cnn_model: str, scale: int, do_compress: bool, quality_factor: int):

        upscaled_img_path = ImgProcesses.upscale_image(
            src_image_path=src_image_path,
            model=cnn_model,
            scale=scale,
        )

        if do_compress:

            print('HERE', flush=True)
            print(quality_factor, flush=True)
            ImgProcesses.compress_image(src_image_path=upscaled_img_path, quality_factor=quality_factor)

        return str(upscaled_img_path)

    @staticmethod
    def enhance_image(src_image: str, img_type: str, enhance_qfactor: int):
        enhanced_image = ImgProcesses.enhance_image(
            src_img=src_image,
            img_type=img_type,
            save_to_path=ImageManager.enhanced_img_path,
            quality_factor=enhance_qfactor,
        )
        return enhanced_image
