from django import views
from django.urls import path
from .views import *

urlpatterns = [
    path("register/",register_view,name="register"),
    path("login/",login_view,name="login"),
    path("refresh-token/",refresh_token_view,name="refresh_token"),
    path("dashboard/",dashboard,name="dashboard"),
    path("logout/",logout_view,name="logout"),
]