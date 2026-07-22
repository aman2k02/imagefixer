from django.db import models
from django.conf import settings


class Image(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="images"
    )

    original_image = models.ImageField(upload_to="original/")

    processed_image = models.ImageField(upload_to="processed/", null=True, blank=True)

    original_name = models.CharField(max_length=255)

    width = models.IntegerField(default=0)

    height = models.IntegerField(default=0)

    file_size = models.BigIntegerField(default=0)

    image_format = models.CharField(max_length=20)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
