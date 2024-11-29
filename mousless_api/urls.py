from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('auth_app.urls')),
    path('', include('problems.urls')),
    path('admin/', admin.site.urls),
]