from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

# class PermissionMixim(object):
#     permission_required = ''

#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             user = request.user

#             # Verificar si el usuario está autenticado
#             # if not user.is_authenticated:
#             #     return redirect(reverse('security:login'))  # Redirigir a la página de inicio de sesión
#             print(user)
#             user.set_group_session()

#             # if 'group_id' not in request.session:
#             #     return redirect('/')

#             if user.is_superuser:
#                 return super().dispatch(request, *args, **kwargs)

#             # group = user.get_group_session()
#             # permissions = self._get_permissions_to_validate()

#             # if not permissions:
#             #     return super().dispatch(request, *args, **kwargs)

#             # if not group.groupmodulepermission_set.filter(
#             #         permissions__codename__in=permissions
#             # ).exists():
#             #     messages.error(request, 'No tiene permiso para ingresar a este módulo')
#             #     return redirect('home')

#             return super().dispatch(request, *args, **kwargs)

#         except Exception as ex:
#             messages.error(request, 'A ocurrido un error al ingresar al modulo, error para el admin es : {}'.format(ex))
#             return redirect('/')

#     # def _get_permissions_to_validate(self):
#     #     if self.permission_required == '':
#     #         return ()

#     #     if isinstance(self.permission_required, str):
#     #         return (self.permission_required,)

#     #     return self.permission_required

class PermissionMixim:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Si el usuario no está autenticado, redirigir a la página de inicio de sesión
            return redirect(reverse('security:login') + '?next=' + request.path)
        
        return super().dispatch(request, *args, **kwargs)