from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from users.views import service_selection

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/v1/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    path('api/v1/users/', include('users.urls')),  # All user-related endpoints under /api/v1/users/
    path('api/v1/chat/', include('chat.urls')),  # All chat-related endpoints under /api/v1/chat/
    path('service-selection/', service_selection, name='service_selection'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
