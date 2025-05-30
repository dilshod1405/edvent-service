from django.urls import path
from authentication.Views.register_view import RegisterView
from authentication.Views.activate_view import activate
from authentication.Views.login_view import LoginView
from authentication.Views.user_detail_view import UserDetailView
from authentication.Views.check_exist_email import check_email_availability
from authentication.Views.check_username_exist import check_username_availability

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path("login/", LoginView.as_view(), name="login"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path('check-email/', check_email_availability, name='check_email_availability'),
    path('check-username/', check_username_availability, name='check_username_availability'),
]