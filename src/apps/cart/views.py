from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db import transaction
from apps.products.models import Product
from .cart import Cart
from apps.cart.services.checkout import (
    validate_checkout_form,
    calculate_totals,
    create_order_with_items,
    update_user_shipping_info,
)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    qty = int(request.POST.get("quantity", 1))
    # validate qty
    if qty < 1:
        qty = 1
    # if needed — check stock
    if product.stock and qty > product.stock:
        qty = product.stock
    cart.add(product=product, quantity=qty, replace_quantity=True)
    # redirect to cart page with # for better UX
    return redirect(reverse("cart:detail") + "#cart")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    cart.remove(product)
    return redirect(reverse("cart:detail") + "#cart")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart})


@require_POST
def cart_update_quantity(request, product_id):
    cart = Cart(request)
    qty = int(request.POST.get("quantity", 1))
    product = get_object_or_404(Product, pk=product_id)
    if qty <= 0:
        cart.remove(product)
    else:
        cart.add(product=product, quantity=qty, replace_quantity=True)
    return redirect(reverse("cart:detail") + "#cart")


@transaction.atomic
def checkout(request):
    cart = Cart(request)
    user = request.user if request.user.is_authenticated else None

    initial = {
        "full_name": getattr(user, "full_name", "") if user else "",
        "phone": getattr(user, "phone", "") if user else "",
        "city": getattr(user, "city", "") if user else "",
        "address": getattr(user, "address", "") if user else "",
    }

    if request.method == "POST":
        form_data = {
            "full_name": request.POST.get("full_name", "").strip(),
            "phone": request.POST.get("phone", "").strip(),
            "city": request.POST.get("city", "").strip(),
            "address": request.POST.get("address", "").strip(),
        }

        valid, error = validate_checkout_form(form_data)
        if not valid:
            return render(
                request,
                "cart/checkout.html",
                {"cart": cart, "initial": form_data, "error": error},
            )

        subtotal = cart.get_subtotal()
        shipping_cost, total = calculate_totals(subtotal)

        shipping_text = (
            f"{form_data['full_name']}\n"
            f"{form_data['phone']}\n"
            f"{form_data['city']}\n"
            f"{form_data['address']}"
        )

        order = create_order_with_items(
            user=user,
            cart=cart,
            shipping_text=shipping_text,
            total_price=total,
        )

        if user and user.is_authenticated:
            update_user_shipping_info(user, form_data)

        cart.clear()

        return render(request, "cart/thankyou.html", {"order": order})

    return render(
        request,
        "cart/checkout.html",
        {"cart": cart, "initial": initial},
    )
