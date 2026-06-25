from django.urls import path

from .views import CustomLoginView, CustomLogoutView, HomeView

urlpatterns = [
    path("auth/login/", CustomLoginView.as_view(), name="login"),
    path("auth/logout/", CustomLogoutView.as_view(), name="logout"),
    path("", HomeView.as_view(), name="home"),
]
