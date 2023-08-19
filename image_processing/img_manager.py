import os

from django.conf import settings

from image_processing.img_processing import ImgProcesses


class ImageManager:
    upscaled_img_path = os.path.join(settings.BASE_DIR, "media/upscaled_images/")
    enhanced_img_path = os.path.join(settings.BASE_DIR, "media/enhanced_images/")

    @staticmethod
    def upscale_image(src_image, cnn_model, scale, user_id, do_compress, quality_factor, enhance_after: bool):
        if enhance_after:
            path = os.path.join(ImageManager.enhanced_img_path, user_id)
        else:
            path = os.path.join(ImageManager.upscaled_img_path, user_id)

        upscaled_img_path = ImgProcesses.upscale_image(
            src_image_bytes=src_image,
            model=cnn_model,
            scale=scale,
            save_to_path=path,
        )

        if do_compress:
            ImgProcesses.compress_image(src_image_path=upscaled_img_path, quality_factor=quality_factor)

        return upscaled_img_path

    @staticmethod
    def enhance_image(src_image, img_type, enhance_qfactor, user_id):
        enhanced_image = ImgProcesses.enhance_image(
            src_img=src_image,
            img_type=img_type,
            save_to_path=os.path.join(ImageManager.enhanced_img_path, user_id),
            quality_factor=enhance_qfactor,
        )
        return enhanced_image
