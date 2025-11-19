from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cart/", include("apps.cart.urls")),
    path("", include("apps.products.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("users/", include("apps.users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
