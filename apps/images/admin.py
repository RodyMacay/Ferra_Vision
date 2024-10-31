from django.contrib import admin

from apps.images.models import ImageUpload, Favorite

# Register your models here.

admin.site.register(ImageUpload)
admin.site.register(Favorite)
