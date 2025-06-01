from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from authentication.permissions import IsAdminUserOnly
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="archedu.uz (edvent.uz) API Documentation",
        default_version='v1',
        description="API documentation for the Archedu platform, formerly known as Edvent.",
    ),
    public=False,
    permission_classes=[IsAdminUserOnly],
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
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)