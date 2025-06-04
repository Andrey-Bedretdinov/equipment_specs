from django.urls import path, include

from apps.catalog.urls import urlpatterns as catalog_urls
from apps.projects.urls import urlpatterns as projects_urls

urlpatterns = [
    path('api/', include(catalog_urls)),
    path('api/', include(projects_urls)),
]