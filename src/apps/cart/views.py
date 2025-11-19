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


@transaction.atomic
def checkout(request):
    """
    Simple realization of order processing:
    - create Order
    - create OrderItem for each position
    - decrease stock
    - clear cart
    """
    cart = Cart(request)
    if request.method == "POST":
        # simple form: shipping_address, maybe phone/email
        shipping = request.POST.get("shipping_address", "")
        if not shipping:
            return render(
                request,
                "cart/checkout.html",
                {"cart": cart, "error": "Enter Shipping Address"},
            )
        # calculate totals
        subtotal = cart.get_subtotal()
        shipping_cost = (
            Decimal("5.00") if subtotal < Decimal("50.00") else Decimal("0.00")
        )
        total = subtotal + shipping_cost

        # create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            status="pending",
            total_price=total,
            shipping_address=shipping,
        )

        # create positions and decrease stock
        for item in cart:
            product = item["product"]
            quantity = item["quantity"]
            price = item["price"]
            OrderItem.objects.create(
                order=order, product=product, quantity=quantity, price=price
            )
            # decrease stock — preliminary check
            if product.stock is not None:
                if product.stock < quantity:
                    # revert transaction
                    raise ValueError(f"Not enough stock for {product.name}")
                product.stock -= quantity
                product.save()

        # here can integrate payment system: create payment intent and redirect
        cart.clear()
        return render(request, "cart/thankyou.html", {"order": order})

    return render(request, "cart/checkout.html", {"cart": cart})
