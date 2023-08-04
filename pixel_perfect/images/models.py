from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class EnhancedImages(models.Model):
    img_name = models.CharField(max_length=100, null=False)
    img_path = models.ImageField(null=True, validators=[FileExtensionValidator(["jpg", "jpeg", "png", "bmp"])])
    img_owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.img_name
