document.addEventListener("DOMContentLoaded", () => {

    const cartPage = document.querySelector(".cart-page-wrapper");
    if (!cartPage) return;

    const cartList = document.getElementById("cart-items-list");

    cartList.addEventListener("click", function (event) {

        const btn = event.target.closest("button");
        if (!btn) return;

        const action = btn.dataset.action;
        const cartItem = btn.closest(".cart-item");

        // Remove button
        if (action === "remove") {
            event.preventDefault();
            btn.closest("form").submit();
            return;
        }

        // Quantity logic
        const qtyForm = cartItem.querySelector(".cart-item__quantity-selector");
        const qtyDisplay = cartItem.querySelector(".quantity-value-cart");
        const qtyInput = cartItem.querySelector(".quantity-input-hidden");

        let qty = parseInt(qtyInput.value);

        // Increase / Decrease
        if (action === "increase") qty++;
        if (action === "decrease") qty--;

        // If qty = 0 → remove item
        if (qty <= 0) {
            event.preventDefault();
            cartItem.querySelector("form[action*='remove']").submit();
            return;
        }

        // Apply UI changes
        qtyInput.value = qty;
        qtyDisplay.textContent = qty;

        // Submit update-form
        event.preventDefault();
        qtyForm.submit();
    });

});
