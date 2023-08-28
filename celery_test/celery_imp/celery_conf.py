from celery import Celery
from image_processing.img_manager import ImageManager


celery_obj = Celery("my_celery", broker="redis://redis:6379/0", backend="redis://redis:6379/0")


@celery_obj.task()
def upscale_image_task(params: dict):
    upscaled_img_path = ImageManager.upscale_image(**params)

    filename = upscaled_img_path.split('/')[-1]
    database_image_path = upscaled_img_path.replace("app/media/", "")

    from celery_imp.models import EnhancedImages
    image_db = EnhancedImages.objects.filter(img_path=database_image_path).first()

    if not image_db:
        image_db = EnhancedImages(
            img_path=database_image_path, img_name=filename)
        image_db.save()

    return {'src': str(image_db.img_path.url), 'id': int(image_db.id)}
