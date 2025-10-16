# apps/show/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .controllers.show_controller import ShowController

router = DefaultRouter()
router.register(r'shows', ShowController, basename='show')

urlpatterns = [
    path('', include(router.urls)),
]
