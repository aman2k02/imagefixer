from django.urls import path
from .views import ImageUploadView,ResizeImageView,ImageListView,ImageDetailView,ImageDeleteView

urlpatterns = [
    path("upload/", ImageUploadView.as_view(), name="upload-image"),
    path("resize/<int:pk>/", ResizeImageView.as_view(), name="resize-image"),
    path("", ImageListView.as_view(), name="image-list"),
    path(
    "<int:pk>/",
    ImageDetailView.as_view(),
    name="image-detail"
),
    path(
    "<int:pk>/delete/",
    ImageDeleteView.as_view(),
    name="image-delete"
),
]