from apps.images.models import ImageUpload, Favorite
from apps.security.mixins.mixim import PermissionMixim
from django.views.generic import ListView

class ListViewsHistoryImage(PermissionMixim, ListView):
    template_name = 'images/history/image_list.html'
    context_object_name = 'images'
    
    def get_queryset(self):
        # Obtiene las imágenes con descripción del usuario actual
        return ImageUpload.objects.get_image_and_description_by_user(self.request.user.username)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user

        # Verifica que el usuario esté autenticado antes de obtener favoritos
        if user.is_authenticated:
            # Obtiene los IDs de las imágenes favoritas del usuario
            favorite_ids = Favorite.objects.filter(user=user).values_list('image_id', flat=True)
            context['favorite_ids'] = list(favorite_ids)  # Convertimos a lista para facilitar su uso en la plantilla
        else:
            context['favorite_ids'] = []

        return context
