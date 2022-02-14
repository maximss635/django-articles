from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('articles.urls')),
    path('auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('registration/', include('registration.urls')),
]
