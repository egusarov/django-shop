import stripe
from decimal import Decimal
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from apps.products.models import Product
from apps.cart.cart import Cart
from apps.orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request):
    cart = Cart(request)

    line_items = []

    product_ids = cart.cart.keys()
    products = Product.objects.filter(pk__in=product_ids)
    products_map = {str(p.pk): p for p in products}

    for product_id, item in cart.cart.items():
        product = products_map[str(product_id)]

        price = Decimal(item["price"])

        line_items.append(
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(price * 100),
                    "product_data": {
                        "name": product.name,
                    },
                },
                "quantity": item["quantity"],
            }
        )

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=line_items,
        success_url=request.build_absolute_uri("/payments/success/"),
        cancel_url=request.build_absolute_uri("/payments/cancel/"),
        metadata={
            "user_id": request.user.id if request.user.is_authenticated else None,
            "shipping_full_name": request.POST.get("full_name", ""),
            "shipping_phone": request.POST.get("phone", ""),
            "shipping_city": request.POST.get("city", ""),
            "shipping_address": request.POST.get("address", ""),
        },
    )

    return redirect(session.url)


def payment_success(request):
    return render(request, "payments/success.html")


def payment_cancel(request):
    return render(request, "payments/cancel.html")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        metadata = session.get("metadata", {})
        user_id = metadata.get("user_id") or None
        amount_total = Decimal(session["amount_total"]) / 100

        shipping_address = (
            f"{metadata.get('shipping_full_name', '')}, "
            f"{metadata.get('shipping_phone', '')}, "
            f"{metadata.get('shipping_city', '')}, "
            f"{metadata.get('shipping_address', '')}"
        )

        Order.objects.create(
            user_id=user_id,
            total_price=amount_total,
            shipping_address=shipping_address,
            status="paid",
        )

    return HttpResponse(status=200)
