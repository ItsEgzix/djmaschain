from django.urls import path
from . import views

urlpatterns = [
    path('', views.fetchdata, name='fetchdata'),
    path('search/', views.search, name='fetchdata'),
]
