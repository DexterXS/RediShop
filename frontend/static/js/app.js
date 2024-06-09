document.addEventListener('DOMContentLoaded', function() {
    // Код для страницы продуктов
    const productGrid = document.getElementById('productGrid');
    const sortPrice = document.getElementById('sortPrice');
    const noProductsMessage = document.getElementById('noProductsMessage');

    if (productGrid && sortPrice && noProductsMessage) {
        let products = [];

        async function fetchProducts() {
            const response = await fetch('/products');
            products = await response.json();
            displayProducts(products);
        }

        function displayProducts(products) {
    const productGrid = document.getElementById('productGrid');
    const noProductsMessage = document.getElementById('noProductsMessage');
    productGrid.innerHTML = '';
    if (products.length === 0) {
        noProductsMessage.style.display = 'block';
    } else {
        noProductsMessage.style.display = 'none';
        products.forEach(product => {
            const productDiv = document.createElement('div');
            productDiv.classList.add('product');
            productDiv.innerHTML = `
                <img src="/static/${product.image_path}" alt="${product.name}">
                <div class="product-details">
                    <h3>${product.name}</h3>
                    <p>Price: $${product.price}</p>
                    <div class="quantity-selector">
                        <button onclick="changeQuantity(this, -1)">-</button>
                        <input type="number" value="1" min="1" max="99" readonly>
                        <button onclick="changeQuantity(this, 1)">+</button>
                    </div>
                    <button onclick="addToCart(${product.id}, this)">Buy</button>
                </div>
            `;
            productGrid.appendChild(productDiv);
        });
    }
}


        function changeQuantity(button, change) {
            const input = button.parentElement.querySelector('input');
            let value = parseInt(input.value) + change;
            if (value < 1) value = 1;
            if (value > 99) value = 99;
            input.value = value;
        }

        async function addToCart(productId, button) {
            const quantity = button.previousElementSibling.querySelector('input').value;
            const response = await fetch('/add_to_cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ productId, quantity })
            });
            if (response.ok) {
                alert('Product added to cart');
                button.previousElementSibling.querySelector('input').value = 1;
                updateCartCount();
            } else {
                alert('Failed to add product to cart');
            }
        }

        async function updateCartCount() {
            const response = await fetch('/cart_count');
            const count = await response.json();
            document.getElementById('cartCount').innerText = `(${count})`;
        }

        sortPrice.addEventListener('change', () => {
            const sortedProducts = [...products];
            sortedProducts.sort((a, b) => {
                if (sortPrice.value === 'asc') {
                    return a.price - b.price;
                } else {
                    return b.price - a.price;
                }
            });
            displayProducts(sortedProducts);
        });

        fetchProducts();
        updateCartCount();
    }

    // Код для страницы добавления продукта
    const addProductForm = document.getElementById('addProductForm');
    if (addProductForm) {
        addProductForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData(addProductForm);

            const response = await fetch('/add_product', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                alert('Product added successfully!');
                addProductForm.reset();
                // Обновите список продуктов
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        });
    }

    // Код для страницы логина
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData(loginForm);

            const response = await fetch('/login', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                window.location.href = '/profile';  // Перенаправляем пользователя на страницу профиля после успешного логина
            } else {
                const errorData = await response.json();
                document.getElementById('errorMessage').innerText = errorData.detail;
            }
        });
    }
});
