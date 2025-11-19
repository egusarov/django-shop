document.addEventListener("DOMContentLoaded", function () {

    /* ============================================================
       2. CATALOG PAGE (home.html)
       Sorting, pagination, filters
    ============================================================ */
    const catalogContent = document.querySelector(".main-content-grid");

    if (catalogContent) {

        /* ---------- 2.1. SORTING ---------- */
        const sortButtons = document.querySelectorAll(".sort-options .sort-button");
        if (sortButtons.length > 0) {
            sortButtons.forEach(button => {
                button.addEventListener("click", function () {
                    sortButtons.forEach(btn => btn.classList.remove("active-sort"));
                    this.classList.add("active-sort");
                });
            });
        }

        /* ---------- 2.2. PAGINATION ---------- */
        const paginationList = document.querySelector(".pagination-list");
        if (paginationList) {
            paginationList.querySelectorAll(".pagination__link").forEach(link => {
                link.addEventListener("click", function () {
                    paginationList.querySelectorAll(".pagination__link").forEach(l => l.classList.remove("active"));
                    this.classList.add("active");
                });
            });
        }

        /* ============================================================
           2.3. FILTERS: categories + keywords
        ============================================================ */
        const keywordsList = document.querySelector(".keywords-list");
        const checkboxes = document.querySelectorAll(".checkbox-group input[type='checkbox']");
        const filterForm = document.getElementById("filter-form");

        if (keywordsList && checkboxes.length > 0 && filterForm) {

            /* ---------- Checkbox -> Tag ---------- */
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener("change", function () {

                    const slug = this.value;

                    if (this.checked) {
                        // Add tag ONLY if not already added
                        if (!document.querySelector(`.keyword-tag[data-slug="${slug}"]`)) {
                            const tag = document.createElement("span");
                            tag.className = "keyword-tag";
                            tag.dataset.slug = slug;
                            tag.innerHTML = `${slug} <i class="fa-solid fa-xmark remove-keyword-icon"></i>`;
                            keywordsList.appendChild(tag);
                        }
                    } else {
                        // Remove tag
                        const tag = document.querySelector(`.keyword-tag[data-slug="${slug}"]`);
                        if (tag) tag.remove();
                    }

                    filterForm.submit();
                });
            });

            /* ---------- Category checkboxes -> URL with hash ---------- */
            document.querySelectorAll('input[name="category"]').forEach(checkbox => {
                checkbox.addEventListener('change', function () {

                    const selected = Array.from(
                        document.querySelectorAll('input[name="category"]:checked')
                    ).map(cb => cb.value);

                    const url = new URL(window.location);

                    url.searchParams.delete("category");
                    selected.forEach(v => url.searchParams.append("category", v));

                    // add hash
                    url.hash = "products";

                    window.location.href = url.toString();
                });
            });

            /* ---------- Tag -> Uncheck checkbox ---------- */
            keywordsList.addEventListener("click", function (event) {
                const icon = event.target.closest(".remove-keyword-icon");
                if (!icon) return;

                const tag = icon.closest(".keyword-tag");
                const slug = tag.dataset.slug;

                // Remove visual tag
                tag.remove();

                // Uncheck checkbox with same slug
                const checkbox = document.querySelector(`input[type="checkbox"][value="${slug}"]`);
                if (checkbox) checkbox.checked = false;

                filterForm.submit();
            });
        }
    }


    /* ============================================================
       3. PRODUCT DETAIL PAGE
    ============================================================ */
    const productPage = document.querySelector(".page-product");

    if (productPage) {

        // Accordion
        const accordionTitle = document.querySelector(".accordion-title");
        if (accordionTitle) {
            accordionTitle.addEventListener("click", function () {
                this.closest(".accordion-item").classList.toggle("active");
            });
        }

        // Cart logic
        const cartControls = document.querySelector(".cart-controls");
        if (cartControls) {
            const addToCartBtn = cartControls.querySelector("#add-to-cart-btn");
            const quantityCounter = cartControls.querySelector("#quantity-counter");
            const decreaseBtn = quantityCounter.querySelector("[data-action='decrease']");
            const increaseBtn = quantityCounter.querySelector("[data-action='increase']");
            const quantityValueSpan = quantityCounter.querySelector(".quantity-value");

            let quantity = 0;

            function update() {
                if (quantity === 0) {
                    addToCartBtn.classList.remove("is-hidden");
                    quantityCounter.classList.add("is-hidden");
                } else {
                    addToCartBtn.classList.add("is-hidden");
                    quantityCounter.classList.remove("is-hidden");
                    quantityValueSpan.textContent = `${quantity} in cart`;
                }
            }

            addToCartBtn.addEventListener("click", function () {
                quantity = 1;
                update();
            });

            decreaseBtn.addEventListener("click", function () {
                if (quantity > 0) {
                    quantity--;
                    update();
                }
            });

            increaseBtn.addEventListener("click", function () {
                quantity++;
                update();
            });

            update();
        }
    }

    /* ============================================================
       5. ACCOUNT / ADMIN PAGES
    ============================================================ */
    const accountOrAdmin = document.querySelector(".account-page-wrapper, .admin-page-wrapper");

    if (accountOrAdmin) {

        // Tabs
        const accountTabs = document.querySelectorAll(".account-tab");
        const tabPanes = document.querySelectorAll(".tab-pane");

        if (accountTabs.length > 0 && tabPanes.length > 0) {
            accountTabs.forEach(tab => {
                tab.addEventListener("click", function () {
                    accountTabs.forEach(t => t.classList.remove("active"));
                    tabPanes.forEach(p => p.classList.remove("active"));

                    const target = document.querySelector(this.dataset.tabTarget);
                    this.classList.add("active");
                    if (target) target.classList.add("active");
                });
            });
        }

        // Category tags
        const categoryTagsContainer = document.querySelector(".category-tags");
        if (categoryTagsContainer) {
            categoryTagsContainer.addEventListener("click", function (e) {
                const tag = e.target.closest(".category-tag");
                if (!tag) return;

                categoryTagsContainer.querySelectorAll(".category-tag")
                    .forEach(t => t.classList.remove("active"));

                tag.classList.add("active");
            });
        }

        // Image upload
        const uploadButton = document.getElementById("upload-image-btn");
        const fileInput = document.getElementById("image-upload-input");

        if (uploadButton && fileInput) {
            uploadButton.addEventListener("click", () => fileInput.click());

            fileInput.addEventListener("change", function (event) {
                const file = event.target.files[0];
                if (!file) return;

                const reader = new FileReader();
                const placeholder = document.querySelector(".image-upload-placeholder");

                reader.onload = function (e) {
                    placeholder.innerHTML = "";
                    placeholder.style.backgroundImage = `url('${e.target.result}')`;
                    placeholder.style.backgroundSize = "cover";
                    placeholder.style.backgroundPosition = "center";
                };

                reader.readAsDataURL(file);
            });
        }
    }


    /* ============================================================
       6. SMOOTH SCROLL TO HASH
    ============================================================ */
    if (window.location.hash) {
        const el = document.querySelector(window.location.hash);
        if (el) el.scrollIntoView({behavior: "smooth"});
    }

});
