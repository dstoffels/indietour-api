from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("/register", views.RegisterView.as_view(), name="register"),
    path("/login", views.LoginView.as_view(), name="login"),
    path("/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("/user", views.UserView.as_view(), name="update user"),
    path("/user/verify", views.UserVerifyView.as_view(), name="verify new user"),
]
