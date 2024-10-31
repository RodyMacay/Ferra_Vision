


from apps.images.models import ImageUpload
from apps.security.mixins.mixim import PermissionMixim
from django.views.generic import ListView

class ListViewsHistoryImage(PermissionMixim, ListView):
    template_name = 'images/history/image_list.html'
    context_object_name = 'images'
    
    def get_queryset(self):
        return ImageUpload.objects.get_image_and_description_by_user(self.request.user.username)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context;