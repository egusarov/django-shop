from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from ..reviews.models import Review


def home(request):
    products = Product.objects.all().annotate(avg_rating=Avg('reviews__rating'))
    categories = Category.objects.all()

    # --- Search ---
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # --- Filter by Category (multiple choice)---
    selected_slugs = request.GET.getlist("category")
    selected_categories = Category.objects.filter(slug__in=selected_slugs)

    if selected_categories:
        products = products.filter(category__slug__in=selected_slugs)

    # --- Sorting ---
    sort_option = request.GET.get('sort', 'new')

    if sort_option == 'price_asc':
        products = products.order_by('price')
    elif sort_option == 'price_desc':
        products = products.order_by('-price')
    elif sort_option == 'rating':
        products = products.order_by('-avg_rating')
    else:  # "new"
        products = products.order_by('-created_at')

    # --- Pagination ---
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # --- form string GET-params without page ---
    qs = request.GET.copy()
    if 'page' in qs:
        qs.pop('page')
    other_qs = qs.urlencode()  # e.g. "q=ale&category=hops&sort=price_desc"
    if other_qs:
        other_qs = '&' + other_qs  # add & to write ?page=2{{ other_qs }}

    context = {
        'products': page_obj,
        'categories': categories,
        'selected_categories': selected_categories,
        'search_query': search_query,
        'sort_option': sort_option,
        'page_obj': page_obj,
        'paginator': paginator,
        'other_qs': other_qs,
    }

    return render(request, 'pages/home.html', context)


def guides_recipes(request):
    return render(request, 'pages/guides_recipes.html')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = Review.objects.filter(product=product).order_by('-created_at')[:3]
    return render(request, 'pages/product_detail.html', {
        'product': product,
        'reviews': reviews
    })
