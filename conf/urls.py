from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", RedirectView.as_view(url="/products/", permanent=False)),
    path("admin/", admin.site.urls),
    path("products/", include("productos.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
