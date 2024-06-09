document.addEventListener('DOMContentLoaded', function() {
    const productGrid = document.getElementById('productGrid');
    const sortPrice = document.getElementById('sortPrice');
    const noProductsMessage = document.getElementById('noProductsMessage');

    let products = [];

    async function fetchProducts() {
        const response = await fetch('/products');
        products = await response.json();
        displayProducts(products);
    }

    function displayProducts(products) {
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
                    <h3>${product.name}</h3>
                    <p>Price: $${product.price}</p>
                    <div class="quantity-selector">
                        <button onclick="changeQuantity(this, -1)">-</button>
                        <input type="number" value="1" min="1" max="99" readonly>
                        <button onclick="changeQuantity(this, 1)">+</button>
                    </div>
                    <button onclick="addToCart(${product.id}, this)">Buy</button>
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
});
