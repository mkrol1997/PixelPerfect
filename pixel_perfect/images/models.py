from django.contrib.auth.models import User
from django.db import models


class EnhancedImages(models.Model):
    img_name = models.CharField(max_length=100, null=False)
    img_path = models.ImageField(null=True)
    img_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(null=False, auto_now=True)

    def __str__(self):
        return self.img_name
