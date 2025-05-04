from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('supercontroller/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('education/', include('education.urls')),
    path('payment/', include('payment.urls')),
    path('auth-base/', include('djoser.urls')),  # Registering the basic auth routes
    path('auth-token/', include('djoser.urls.authtoken')),  # Token-based auth routes
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)