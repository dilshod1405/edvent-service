from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from authentication.permissions import IsAdminUserOnly
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


swagger_view = SpectacularSwaggerView.as_view(
    permission_classes=[IsAdminUserOnly]
)

redoc_view = SpectacularRedocView.as_view(
    permission_classes=[IsAdminUserOnly]
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

    # OpenAPI schema fayl (admin yoki auth talab qilmaydi odatda)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('api/docs/', swagger_view, name='swagger-ui'),

    # Redoc UI (ixtiyoriy)
    path('api/redoc/', redoc_view, name='redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)