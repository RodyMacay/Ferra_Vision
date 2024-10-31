from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from apps.images.models import Favorite, ImageUpload
from apps.security.mixins.mixim import PermissionMixim


class FavoriteListView(PermissionMixim, ListView):
    model = Favorite
    template_name = 'images/favorites/favorites_list.html'  # Nombre de la plantilla a utilizar
    context_object_name = 'favorites'  # Nombre del contexto en la plantilla

    def get_queryset(self):
        # Filtra los favoritos del usuario actual
        return Favorite.objects.get_favorites_by_user(self.request.user.username);
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    
class ToggleFavoriteView(PermissionMixim, View):
    def post(self, request, image_id):
        image = get_object_or_404(ImageUpload, id=image_id)
        
        # Añade o elimina la imagen de favoritos
        favorite, created = Favorite.objects.get_or_create(user=request.user, image=image)
        
        if not created:
            favorite.delete()
        
        # Redirige a la página actual, obtenida de 'HTTP_REFERER'
        return redirect(request.META.get('HTTP_REFERER', 'images:history_upload_image'))
