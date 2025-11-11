from django.shortcuts import render, get_object_or_404
from .models import Product
from ..reviews.models import Review


def home(request):
    products = Product.objects.all()
    return render(request, 'pages/home.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = Review.objects.filter(product=product).order_by('-created_at')[:3]
    return render(request, 'pages/product_detail.html', {
        'product': product,
        'reviews': reviews
    })
