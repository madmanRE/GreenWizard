from django.urls import path
from .views import index, GameListView

app_name = 'catalog'

urlpatterns = [
    path('', index, name='index'),
]
