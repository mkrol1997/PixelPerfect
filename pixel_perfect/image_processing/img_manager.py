from image_processing.img_processing import ImgProcesses


class ImageManager:
    @staticmethod
    def upscale_image(src_image_path: str, cnn_model: str, scale: int, do_compress: bool, quality_factor: int):
        upscaled_img_path = ImgProcesses.upscale_image(
            src_image_path=src_image_path,
            model=cnn_model,
            scale=scale,
        )

        if do_compress:
            ImgProcesses.compress_image(src_image_path=upscaled_img_path, quality_factor=quality_factor)

        return upscaled_img_path

    @staticmethod
    def enhance_image(src_image_path, img_type, enhance_qfactor):
        enhanced_image = ImgProcesses.enhance_image(
            src_image_path=src_image_path,
            img_type=img_type,
            quality_factor=enhance_qfactor,
        )
        return enhanced_image
