from django.urls import path
from authentication.Views.register_view import RegisterView
from authentication.Views.activate_view import activate
from authentication.Views.login_view import LoginView
from authentication.Views.user_detail_view import UserDetailView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path("login/", LoginView.as_view(), name="login"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]