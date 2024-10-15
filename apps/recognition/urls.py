from django.urls import path

from apps.recognition.views.image_upload import ImageUploadView

app_name = "recognition"
urlpatterns = []

urlpatterns += [
    path('image_upload/', ImageUploadView.as_view(), name='image_upload'),

]
