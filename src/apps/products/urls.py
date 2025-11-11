from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('guides-recipes', views.guides_recipes, name='guides-recipes'),
    path("<slug:slug>/", views.product_detail, name="product-detail"),
]
