from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("/register", views.RegisterView.as_view(), name="register"),
    path("/login", views.LoginView.as_view(), name="login"),
    path("/logout", views.LogoutView.as_view(), name="logout"),
    path("/refresh", views.RefreshView.as_view(), name="token_refresh"),
    path("/user", views.UserView.as_view(), name="update user"),
    path("/verify", views.UserVerifyView.as_view(), name="verify new user"),
    path("/password", views.UserPasswordView.as_view(), name="update password"),
]
