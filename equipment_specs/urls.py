from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from apps.catalog.urls import urlpatterns as catalog_urls
from apps.projects.urls import urlpatterns as projects_urls

urlpatterns = [
    path('api/', include(catalog_urls)),
    path('api/', include(projects_urls)),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
