from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("/register", views.RegisterView.as_view(), name="register"),
    # path("/login", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("/login/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    # path("/user", views.update_user),
    # path("/user/<uuid:uid>", views.new_user),
]
