from django.db import models
from django.core.files.storage import FileSystemStorage


class NutritionalLabel(models.Model):
    image = models.ImageField(upload_to="nutritional_label/", unique=True)
