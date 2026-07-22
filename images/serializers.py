from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = "__all__"

        read_only_fields = (
            "user",
            "processed_image",
            "width",
            "height",
            "file_size",
            "image_format",
            "status",
            "created_at",
            "updated_at",
        )
