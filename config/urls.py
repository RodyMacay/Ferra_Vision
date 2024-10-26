from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.security.urls')),
    path('', include('apps.core.urls')),
    path('', include('apps.recognition.urls')),
    path('images/', include(('apps.images.urls', 'images'), namespace='images')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
