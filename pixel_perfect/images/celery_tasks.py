from datetime import date

from celery import Celery
from image_processing.img_manager import ImageManager


celery_obj = Celery("pixel_perfect", broker="redis://redis:6379/0", backend="redis://redis:6379/0")


@celery_obj.task()
def upscale_image_task(params: dict, user_id: int):
    upscaled_img_path = ImageManager.upscale_image(**params)

    filename = upscaled_img_path.split('/')[-1]
    database_image_path = upscaled_img_path.replace("app/media/", "")

    from images.models import EnhancedImages
    from django.contrib.auth.models import User

    image_db, _ = EnhancedImages.objects.update_or_create(
        img_path=database_image_path,
        img_name=filename,
        img_owner=User.objects.get(pk=user_id),
    )

    return {'src': str(image_db.img_path.url), 'id': int(image_db.id)}


@celery_obj.task()
def enhance_image_task(params: dict, user_id):
    enhanced_img_path = ImageManager.enhance_image(**params)

    filename = enhanced_img_path.split('/')[-1]
    database_image_path = enhanced_img_path.replace("app/media/", "")

    from images.models import EnhancedImages
    from django.contrib.auth.models import User

    image_db, _ = EnhancedImages.objects.update_or_create(
        img_path=database_image_path,
        img_name=filename,
        img_owner=User.objects.get(pk=user_id),
        date_created=date.today()
    )
    return {'src': str(image_db.img_path.url), 'id': int(image_db.id)}


@celery_obj.task()
def image_restoration_task(upscale_img_params, enhance_img_params, user_id):
    img_path = ImageManager.upscale_image(**upscale_img_params)
    ImageManager.enhance_image(**enhance_img_params)

    filename = img_path.split('/')[-1]
    database_image_path = img_path.replace("app/media/", "")

    from images.models import EnhancedImages
    from django.contrib.auth.models import User

    image_db, _ = EnhancedImages.objects.update_or_create(
        img_path=database_image_path,
        img_name=filename,
        img_owner=User.objects.get(pk=user_id),
        date_created=date.today()
    )
    return {'src': str(image_db.img_path.url), 'id': int(image_db.id)}
