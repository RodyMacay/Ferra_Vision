from django.urls import path
from apps.images.views.images import ImageDetailView, ImageUploadView, calculate_prices_view

app_name = "images"

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='upload_image'),
    path('<int:pk>/', ImageDetailView.as_view(), name='image_detail'),
    path('<int:pk>/calculate-prices/', calculate_prices_view, name='calculate_prices'),
]
