from django.contrib import admin
from django.urls import path

from .views import get_or_create_cats

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cats/', get_or_create_cats),
]
