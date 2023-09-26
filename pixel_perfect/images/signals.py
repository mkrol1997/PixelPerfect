import os
from shutil import rmtree

from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from image_processing.config import enhanced_img_path, upscaled_img_path


@receiver(post_save, sender=User)
def create_user_img_dirs(sender, instance, created, **kwargs):
    if created:
        os.mkdir(os.path.join(upscaled_img_path, str(instance.id)))
        os.mkdir(os.path.join(enhanced_img_path, str(instance.id)))


@receiver(post_delete, sender=User)
def delete_user_img_dirs(sender, instance, using, **kwargs):
    rmtree(os.path.join(upscaled_img_path, str(instance.id)))
    rmtree(os.path.join(enhanced_img_path, str(instance.id)))
