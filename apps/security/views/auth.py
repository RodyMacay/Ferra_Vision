from django.contrib.auth.views import LoginView
from django.forms import BaseModelForm
from django.http import HttpRequest
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
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= 'Register'
        context['grabar']= 'Register'
        return context
    
    
@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('security:login')