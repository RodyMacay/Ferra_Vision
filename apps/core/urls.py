from django.urls import path
from apps.core.views.home import  HomeView


app_name = "core"
urlpatterns = []

urlpatterns += [
    path('', HomeView.as_view(), name='home'),
]
