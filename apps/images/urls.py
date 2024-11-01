from django.urls import path
from apps.images.views.favorities import FavoriteListView, ToggleFavoriteView
from apps.images.views.history import ListViewsHistoryImage
from apps.images.views.images import ImageDetailView, ImageUploadView, calculate_prices_view

app_name = "images"

urlpatterns = []

urlpatterns +=[
    path('upload/', ImageUploadView.as_view(), name='upload_image'),
    path('<int:pk>/', ImageDetailView.as_view(), name='image_detail'),
    path('<int:pk>/calculate-prices/', calculate_prices_view, name='calculate_prices'),
]

urlpatterns +=[
    path('history/', ListViewsHistoryImage.as_view(), name='history_upload_image'),
    
]


urlpatterns +=[
    path('favorites/', FavoriteListView.as_view(), name='favorites_list'),
    path('toggle_favorite/<int:image_id>/', ToggleFavoriteView.as_view(), name='toggle_favorite')
]
