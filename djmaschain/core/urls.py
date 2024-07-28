from django.urls import path
from . import views

urlpatterns = [
    path('fetchdata/', views.fetchdata, name='fetchdata'),
    path('search/', views.search, name='search'),
    path('', views.landing_page, name='index'),
    path('home/', views.landing_page, name='index'),
    path('404/', views.notfound, name='404'),
]
