from decimal import Decimal
from apps.products.models import Product

CART_SESSION_ID = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, quantity=1, replace_quantity=False, extra=None):
        """
        Add product or update quantity.
        extra — optional dict for options (size, measure...), can save as JSON-serializable.
        """
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }
            if extra:
                self.cart[product_id]["extra"] = extra
        if replace_quantity:
            self.cart[product_id]["quantity"] = int(quantity)
        else:
            self.cart[product_id]["quantity"] += int(quantity)
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product: Product):
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Loop through the elements, add object Product and calculate total
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(pk__in=product_ids)
        products_map = {str(p.pk): p for p in products}
        for pid, item in list(self.cart.items()):
            product = products_map.get(pid)
            if product is None:
                # if product removed from db — remove from cart
                del self.cart[pid]
                self.save()
                continue
            item = item.copy()
            item["product"] = product
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """Quantity of positions"""
        return sum(item["quantity"] for item in self.cart.values())

    def get_subtotal(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self):
        self.session.pop(CART_SESSION_ID, None)
        self.save()
