from decimal import Decimal
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db import transaction
from apps.products.models import Product
from apps.orders.models import Order, OrderItem
from .cart import Cart


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


# ruff: noqa: C901
@transaction.atomic
def checkout(request):
    """
    Order flow:
    - GET: show checkout form with initial shipping fields
    - POST: validate, calculate totals, create Order + OrderItems,
      decrease stock, store shipping info in user (if fields exist),
      clear cart and show thank-you page.
    """
    cart = Cart(request)

    user = request.user if request.user.is_authenticated else None

    initial = {
        "full_name": getattr(user, "full_name", "") if user else "",
        "phone": getattr(user, "phone", "") if user else "",
        "city": getattr(user, "city", "") if user else "",
        "address": getattr(user, "address", "") if user else "",
    }

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        city = request.POST.get("city", "").strip()
        address = request.POST.get("address", "").strip()

        posted = {
            "full_name": full_name,
            "phone": phone,
            "city": city,
            "address": address,
        }

        if not full_name:
            return render(
                request,
                "cart/checkout.html",
                {
                    "cart": cart,
                    "initial": posted,
                    "error": "Enter full name",
                },
            )

        if not address:
            return render(
                request,
                "cart/checkout.html",
                {
                    "cart": cart,
                    "initial": posted,
                    "error": "Enter shipping address",
                },
            )

        subtotal = cart.get_subtotal()
        shipping_cost = (
            Decimal("5.00") if subtotal < Decimal("50.00") else Decimal("0.00")
        )
        total = subtotal + shipping_cost

        shipping_text = f"{full_name}\n{phone}\n{city}\n{address}"

        order = Order.objects.create(
            user=user if user and user.is_authenticated else None,
            status="pending",
            total_price=total,
            shipping_address=shipping_text,
        )

        for item in cart:
            product = item["product"]
            quantity = int(item["quantity"])
            price = item["price"]

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
            )

            if hasattr(product, "stock") and product.stock is not None:
                if product.stock < quantity:
                    raise ValueError(f"Not enough stock for {product.name}")
                product.stock -= quantity
                product.save()

        if user and user.is_authenticated:
            changed = False
            if hasattr(user, "full_name"):
                user.full_name = full_name
                changed = True
            if hasattr(user, "phone"):
                user.phone = phone
                changed = True
            if hasattr(user, "city"):
                user.city = city
                changed = True
            if hasattr(user, "address"):
                user.address = address
                changed = True
            if changed:
                user.save()

        cart.clear()

        return render(
            request,
            "cart/thankyou.html",
            {"order": order},
        )

    return render(
        request,
        "cart/checkout.html",
        {
            "cart": cart,
            "initial": initial,
        },
    )
