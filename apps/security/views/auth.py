from django.contrib.auth.views import LoginView
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from apps.security.forms.auth_forms import CustomAuthenticationForm, CustomUserCreationForm


class LogLoginView(LoginView):
    template_name = 'auth/login.html'
    authentication_form = CustomAuthenticationForm
    
    def dispatch(self, request, *args, **kwargs):
        print("==>", request)
        if request.user.is_authenticated:
            return redirect('/') 
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='Login'
        context['grabar']='Login'
        return context
    
class RegisterView(CreateView):
    template_name = 'auth/register.html'
    success_url = reverse_lazy('security:login')
    form_class = CustomUserCreationForm

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm):
        # Guardar el nuevo usuario
        user = form.save()  # Guarda el usuario aquí
        return super().form_valid(form)  # Llamar al método de la clase padre

    def form_invalid(self, form: BaseModelForm):
        # Guardar los mensajes de error en la sesión
        error_messages = form.errors.as_json()  # Obtener errores del formulario en formato JSON
        self.request.session['error_messages'] = error_messages  # Guardar en la sesión
        return super().form_invalid(form)  # Dejar que el CreateView maneje el formulario inválido

    def get_success_url(self):
        return self.success_url  # Retornar la URL de éxito

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        context['grabar'] = 'Register'
        return context
    
    
@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('security:login')