from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

from .validators import ImageValidator


class EnhancedImages(models.Model):
    img_name = models.CharField(max_length=100, null=False)
    img_path = models.ImageField(
        null=True,
        validators=[ImageValidator(size=1, width=1920, height=1080), FileExtensionValidator(["jpg", "jpeg", "png"])],
    )
    img_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(null=False)

    def __str__(self):
        return self.img_name
