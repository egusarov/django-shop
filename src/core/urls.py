from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include


def index(request):
    return HttpResponse("Магазин работает!")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    # path('', include("apps.products.urls")),
]
