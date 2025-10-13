from django.urls import path
from .controllers.user_controller import UserController

user_register = UserController.as_view({"post": "register"})
user_login = UserController.as_view({"post": "login"})

urlpatterns = [
    path("register/", user_register, name="user-register"),
    path("login/", user_login, name="user-login"),
]
