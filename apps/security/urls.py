from django.urls import path

from apps.security.views.auth import LogLoginView, RegisterView, cerrarSesion
from apps.security.views.user import LogSignUpView

app_name = "security"
urlpatterns = []

urlpatterns += [
    path('login/', LogLoginView.as_view(), name='login'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('logout/', cerrarSesion, name='logout'),
]
