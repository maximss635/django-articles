from django.urls import path, include
from . import views


urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('registration', views.registration, name='registration'),
    path('', include('django.contrib.auth.urls')),
]
