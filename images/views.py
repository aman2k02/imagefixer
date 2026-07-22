import os
from django.core.files import File
from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image as PILImage

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .models import Image
from .serializers import ImageSerializer


class ImageUploadView(generics.CreateAPIView):

    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        uploaded_file = self.request.FILES["original_image"]

        img = PILImage.open(uploaded_file)

        serializer.save(
            user=self.request.user,
            original_name=uploaded_file.name,
            width=img.width,
            height=img.height,
            file_size=uploaded_file.size,
            image_format=img.format,
        )


class ResizeImageView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:
            image = Image.objects.get(pk=pk, user=request.user)

        except Image.DoesNotExist:
            return Response(
                {"error": "Image not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        width = int(request.data.get("width"))
        height = int(request.data.get("height"))
        if width is None or height is None:
            return Response(
                {"error": "Both width and height are required."}, status=400
            )

        width = int(width)
        height = int(height)

        img = PILImage.open(image.original_image.path)

        resized = img.resize((width, height))

        original_name = os.path.basename(image.original_image.name)

        filename, extension = os.path.splitext(original_name)

        new_filename = f"{filename}_{width}x{height}{extension}"

        processed_dir = os.path.join("media", "processed")

        os.makedirs(processed_dir, exist_ok=True)

        save_path = os.path.join(processed_dir, new_filename)

        resized.save(save_path)

        with open(save_path, "rb") as f:
            image.processed_image.save(
                new_filename,
                File(f),
                save=False,
            )

        image.status = "COMPLETED"
        image.save()

        return Response(
            {
                "message": "Image resized successfully",
                "processed_image": image.processed_image.url,
                "status": image.status,
            }
        )


class ImageListView(generics.ListAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user).order_by("-created_at")


class ImageDetailView(generics.RetrieveAPIView):

    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print("Logged in user:", self.request.user.id)
        print(Image.objects.values("id", "user_id"))
        return Image.objects.filter(user=self.request.user)


class ImageDeleteView(generics.DestroyAPIView):

    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):

        if instance.original_image:
            instance.original_image.delete(save=False)

        if instance.processed_image:
            instance.processed_image.delete(save=False)

        instance.delete()
