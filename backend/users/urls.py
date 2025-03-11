from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import RegisterUser

# Crie um roteador para o ViewSet
router = DefaultRouter()
router.register(r'users', RegisterUser, basename='registre')

# Inclua as rotas do roteador no seu urls.py
urlpatterns = [
    path('', include(router.urls)),
]