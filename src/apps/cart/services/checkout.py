from decimal import Decimal
from apps.orders.models import Order, OrderItem


def validate_checkout_form(data):
    required = ["full_name", "phone", "city", "address"]

    for field in required:
        if not data.get(field, "").strip():
            return False, f"Field “{field}” is required."

    return True, None


def calculate_totals(subtotal):
    shipping_cost = Decimal("5.00") if subtotal < Decimal("50.00") else Decimal("0.00")
    total = subtotal + shipping_cost
    return shipping_cost, total


def create_order_with_items(user, cart, shipping_text, total_price):
    order = Order.objects.create(
        user=user,
        status="pending",
        shipping_address=shipping_text,
        total_price=total_price,
    )

    for item in cart:
        product = item["product"]
        quantity = item["quantity"]
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

    return order


def update_user_shipping_info(user, data):
    changed = False

    for field in ["full_name", "phone", "city", "address"]:
        if hasattr(user, field):
            setattr(user, field, data[field])
            changed = True

    if changed:
        user.save()
